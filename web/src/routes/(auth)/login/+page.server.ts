import { cb } from '$lib/utils/auth';
import { PROD } from '$env/static/private';
import {db} from '$lib/utils/surreal-client';
import { rootdb } from '$lib/utils/surreal-root';
import { redirect } from '@sveltejs/kit';

export const load = async ({ url, cookies }) => {
	const code = url.searchParams.get('code');
	if (!code) {
		throw redirect(302, '/');
	}

	const {access_token} = await cb.exchangeInitialToken(code);

	if (!access_token) {
		throw redirect(302, '/');
	}

	cookies.set('cb_token', access_token, {
		path: '/',
		expires: new Date(Date.now() + 1000 * 60 * 60 * 24 * 7),
		httpOnly: true,
		sameSite: PROD === 'true' ? 'none' : 'lax',
    secure: PROD === 'true',
	});

	const user = await cb.getUserInfo(access_token);

	// check if user id exists in database user table
	let userExists = await rootdb.select(`user:${user.id}`);

	// if not, create user in database user table
	if (!userExists) {
		userExists = await rootdb.create(`user:${user.id}`, {
			avatar: user.avatar,
			name: user.name
		})
	} 

	const signup = await db.signup({
		scope: 'dash_session',
		owner: `user:${user.id}`,
		cb_token: access_token
	})

	cookies.set('session', signup, {
		path: '/',
		expires: new Date(Date.now() + 1000 * 60 * 60),
		httpOnly: true,
		sameSite: PROD === 'true' ? 'none' : 'lax',
    secure: PROD === 'true',
	})

	throw redirect(302, '/');
};