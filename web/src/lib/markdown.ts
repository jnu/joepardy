import { Marked } from 'marked';

const renderer = new Marked();

export const markdown = (text: string) => {
    return renderer.parse(text);
};