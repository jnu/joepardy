export const clean = (str: string) => {
	return str.replace(/\\(["'])/g, '$1');
};


export type Answer = {
	text: string;
	meta?: string;
}

const CLUE_CREW_PAT = /^(\(.*?clue crew.*?\))/i;

export const splitAnswer = (str: string): Answer => {
	const match = str.match(CLUE_CREW_PAT);
	if (match) {
		const meta = match[1];
		const text = str.replace(CLUE_CREW_PAT, '').trim();
		return { text, meta };
	}

	return { text: str, meta: undefined };
}

export const parse = (str: string) => {
	const cleaned = clean(str);
	return splitAnswer(cleaned);
}
