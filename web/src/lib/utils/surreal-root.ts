import { SURREAL_ROOT_PASSWORD, SURREAL_ROOT_USER } from '$env/static/private';
import { PUBLIC_SURREAL_DB, PUBLIC_SURREAL_NS, PUBLIC_SURREAL_URL } from '$env/static/public';

import Surreal from 'surrealdb.js';

const MAX_RETRIES = 5;
const RETRY_TIMEOUT = 2000; // 2 seconds
const DB_URL = PUBLIC_SURREAL_URL;
let _db: Surreal;

const database = {
	get instance() {
		if (!_db) {
			let retries = 1;

			const tryConnect = async () => {
				try {
					if (retries > 1) {
						console.log(`Database connection retry, attempt number ${retries} of ${MAX_RETRIES}`);
					}
					_db = new Surreal();

					if (!DB_URL) return null;
					await _db.connect(DB_URL, { namespace: PUBLIC_SURREAL_NS, database: PUBLIC_SURREAL_DB, auth: {
						username: SURREAL_ROOT_USER,
						password: SURREAL_ROOT_PASSWORD
					} });
				} catch (error) {
					if (retries < MAX_RETRIES) {
						retries++;
						setTimeout(tryConnect, RETRY_TIMEOUT);
					} else {
						console.log('Database connection failed.');
						throw error;
					}
				}
			};

			tryConnect();
		}
		return _db;
	},
};

export const rootdb = database.instance;