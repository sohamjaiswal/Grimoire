import {redirect} from "@sveltejs/kit"
import {cb} from "$lib/utils/auth"
import { PROD } from "$env/static/private"

export const load = () => {
  throw redirect( 302, '/') 
}

export const actions = {
  default: async({cookies, locals}) => {
    const code = cookies.get('cb_token')
    const db_token = cookies.get('session');
    if (!code) {
      throw redirect( 302, '/')
    }
    cb.revokeToken(code)
    if (db_token) {
      const auth = await locals.db.info();
      if (auth) {
        console.log(auth)
        await locals.db.delete(auth.id);
        await locals.db.invalidate()
      }
    }
    cookies.set('cb_token', '', {
			path: '/',
			expires: new Date(0),
      sameSite: PROD === 'true' ? 'none' : 'lax',
      secure: PROD === 'true',
		})
    cookies.set('session', '', {
      path: '/',
      expires: new Date(0),
      sameSite: PROD === 'true' ? 'none' : 'lax',
      secure: PROD === 'true'
    })
    throw redirect( 302, '/')
  }
}