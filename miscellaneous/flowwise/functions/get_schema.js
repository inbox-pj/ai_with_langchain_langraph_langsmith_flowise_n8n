const { DataSource } = require('typeorm');

// const HOST = 'pgvector';
const HOST = 'localhost';
const USER = 'postgres';
const PASSWORD = 'postgres';
const DATABASE = 'vectord_db';
const PORT = 5432;

const AppDataSource = new DataSource({
    type: 'postgres',
    host: HOST,
    port: PORT,
    username: USER,
    password: PASSWORD,
    database: DATABASE,
    synchronize: false,
    logging: false,
});

async function getSQLPrompt() {
    let sqlSchemaPrompt = '';
    try {
        await AppDataSource.initialize();
        const queryRunner = AppDataSource.createQueryRunner();

        const tablesResult = await queryRunner.query(`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    `);

        for (const tableRow of tablesResult) {
            const tableName = tableRow.table_name;

            const schemaInfo = await queryRunner.query(
                `SELECT column_name, data_type, is_nullable
         FROM information_schema.columns
         WHERE table_name = $1`,
                [tableName]
            );

            const createColumns = [];
            const columnNames = [];

            for (const column of schemaInfo) {
                const name = column.column_name;
                const type = column.data_type.toUpperCase();
                const notNull = column.is_nullable === 'NO' ? 'NOT NULL' : '';
                columnNames.push(name);
                createColumns.push(`${name} ${type} ${notNull}`);
            }

            const sqlCreateTableQuery = `CREATE TABLE ${tableName} (${createColumns.join(', ')})`;
            const sqlSelectTableQuery = `SELECT * FROM ${tableName} LIMIT 3`;

            let allValues = [];
            try {
                const rows = await queryRunner.query(sqlSelectTableQuery);
                allValues = rows.map(row =>
                    columnNames.map(col => row[col]).join(' ')
                );
            } catch (err) {
                allValues.push('[ERROR FETCHING ROWS]');
            }

            sqlSchemaPrompt +=
                sqlCreateTableQuery +
                '\n' +
                sqlSelectTableQuery +
                '\n' +
                columnNames.join(' ') +
                '\n' +
                allValues.join('\n') +
                '\n\n';
        }

        await queryRunner.release();
        return sqlSchemaPrompt;
    } catch (err) {
        console.error(err);
        throw err;
    }
}

async function main() {
    const schema = await getSQLPrompt();
    return schema;
}

// Usage example:
main().then(schema => {
    console.log(schema);
});