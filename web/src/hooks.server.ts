import { PROD } from "$env/static/private";
import {cb} from "$lib/utils/auth"
import type { Handle } from "@sveltejs/kit";
import {db} from '$lib/utils/surreal-client';

const auth: Handle = (async ({ event, resolve }) => {
  const token = event.cookies.get('cb_token');
  if (token) {
    try {
      const db_token = event.cookies.get('session');
      const user = await cb.getUserInfo(token);

      // try authenticating with database
      if (db_token && user && user.id) {
        const auth = await db.authenticate(db_token);
        if (!auth) {
          const signup = await db.signup({
            scope: 'dash_session',
            owner: `user:${user.id}`,
            cb_token: token
          })
          event.cookies.set('session', signup, {
            path: '/',
            expires: new Date(Date.now() + 1000 * 60 * 60),
            sameSite: PROD === 'true' ? 'none' : 'lax',
            secure: PROD === 'true'
          })
        }
      }
      if (!user || !user.id || user.id == '') {
        event.cookies.set('session', '', {
          path: '/',
          expires: new Date(0),
          sameSite: PROD === 'true' ? 'none' : 'lax',
          secure: PROD === 'true'
        });
        if (db_token) {
          const auth = await db.info();
          if (auth) await db.delete(auth.id);
          await db.invalidate()
        }
        event.locals.db = db;
        return resolve(event);
      }
      event.locals.db = db;
      event.locals.user = user;
    } catch {
      event.cookies.delete('cb_token', { path: '/' });
      event.cookies.delete('session', { path: '/' });
    }
  }
  // user passed only if token was valid and got data
  event.locals.db = db;
  return resolve(event);
});

export const handle = auth;