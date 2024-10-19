<script lang="ts">
	import { goto } from '$app/navigation';
	import { clean } from '$lib/clean';
	export let data;

	$: explanation = data.explanation;

	async function back() {
		await goto(`/trivia/${explanation.trivium.id}`);
	}

	async function next() {
		await goto(`/`);
	}
</script>

<div class="flex flex-col space-y-2 h-screen">
	<div class="text-m text-slate-600 text-center w-full py-2 dark:bg-blue-500">
		{clean(explanation.trivium.category)} - ${explanation.trivium.score}
	</div>
	<div class="text-sm text-slate-900 self-center px-2">
		{clean(explanation.trivium.answer)}:
		<span class="font-bold">{clean(explanation.trivium.question)}</span>
	</div>
	<div
		class="text-m text-slate-900 dark:text-white text-left overflow-y-auto px-2 border border-blue-300"
	>
		<span class="font-bold">Summary:&nbsp;</span>{explanation.summary.content}
	</div>
	<div class="!mt-auto w-full flex">
		<button
			on:click={back}
			class="bg-red-500 hover:bg-red-600 dark:text-white font-bold py-2 px-4 text-2xl basis-1/2"
			>back</button
		>
		<button
			on:click={next}
			class="bg-green-500 hover:bg-green-600 dark:text-white font-bold py-2 px-4 text-2xl basis-1/2"
			>next</button
		>
	</div>
</div>
