import { CB_TOKEN, CB_SECRET } from '$env/static/private';
import { Cardboard } from 'cardboard.js';

if (!CB_TOKEN) {
	throw new Error('Missing Cardboard Token');
}

if (!CB_SECRET) {
	throw new Error('Missing Cardboard Secret');
}

export const cb = new Cardboard(CB_TOKEN, CB_SECRET);