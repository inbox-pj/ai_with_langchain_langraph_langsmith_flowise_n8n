const { DataSource } = require('typeorm');

// Configuration
const HOST = 'localhost';
const USER = 'postgres';
const PASSWORD = 'postgres';
const DATABASE = 'vectord_db';
const PORT = 5432;

// Replace with your actual query string
const sqlQuery = 'SELECT * FROM your_table LIMIT 3';

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

async function runSQLQuery(query) {
    let formattedResult = '';
    try {
        await AppDataSource.initialize();
        const queryRunner = AppDataSource.createQueryRunner();

        const rows = await queryRunner.query(query);

        if (rows.length === 0) {
            formattedResult = '[No results returned]';
        } else {
            const columnNames = Object.keys(rows[0]);
            const header = columnNames.join(' ');
            const values = rows.map(row =>
                columnNames.map(col => row[col]).join(' ')
            );
            formattedResult = query + '\n' + header + '\n' + values.join('\n');
        }

        await queryRunner.release();
    } catch (err) {
        console.error('[ERROR]', err);
        formattedResult = `[Error executing query]: ${err}`;
    }
    return formattedResult;
}

async function main() {
    const result = await runSQLQuery(sqlQuery);
    console.log(result);
}

main();