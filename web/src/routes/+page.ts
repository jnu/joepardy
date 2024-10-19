import type {PageLoad} from './$types';
import * as api from '$lib/api';

export const load: PageLoad = async ({fetch}) => {
    return {
        trivium: await api.getRandomQuestion(fetch)
    }
}