import type { PageLoad } from './$types';
import * as api from '$lib/api';

export const load: PageLoad = async ({ fetch, params }) => {
	return {
		trivium: await api.getQuestion(fetch, params.id)
	};
};
