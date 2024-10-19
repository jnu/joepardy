import type { PageLoad } from './$types';
import * as api from '$lib/api';
import { redirect } from '@sveltejs/kit';

export const load: PageLoad = async ({ fetch }) => {
	const id = await api.getRandomId(fetch);
	return redirect(302, `/trivia/${id}`);
};
