import { redirect } from "@sveltejs/kit"
import { PUBLIC_CB_URL } from "$env/static/public"
export const load = async ({ locals }) => {
	// redirect user if logged in
	if (!locals.user) {
		throw redirect(302, PUBLIC_CB_URL)
	}
}