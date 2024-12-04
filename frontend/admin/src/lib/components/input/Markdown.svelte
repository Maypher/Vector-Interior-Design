<script lang="ts">
	import '$lib/styles/markdown.css';
	import { onMount } from 'svelte';
	import * as markdown from '$lib/utilities/markdown';

	let preview: boolean = $state(false);

	let { content = $bindable('') } = $props();

	let textArea: HTMLTextAreaElement = $state()!;

	function setPreview(val: boolean) {
		preview = val;
	}

	// Updates a list when Enter is pressed.
	onMount(() => markdown.updateListOnEnter(textArea));
</script>

<div class="max-w-xl">
	<div class="flex justify-between items-center text-gray-400 bg-gray-700 rounded-t-md">
		<div class="h-12 mx-3">
			<button
				type="button"
				class="hover:text-white h-full px-2"
				class:bg-black={!preview}
				class:border-x-2={!preview}
				class:text-white={!preview}
				onclick={() => setPreview(false)}>Editar</button
			>
			<button
				type="button"
				class="hover:text-white h-full px-2"
				class:bg-black={preview}
				class:border-x-2={preview}
				class:text-white={preview}
				onclick={() => setPreview(true)}>Observar</button
			>
		</div>
		{#if !preview}
			<div class="flex items-center mx-2">
				<button
					type="button"
					class="font-bold hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.boldText(textArea);
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}>N</button
				>
				<button
					type="button"
					class="italic hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.italicText(textArea);
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}>I</button
				>
				<button
					type="button"
					class=" hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.titleText(textArea);
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}>T</button
				>
				<button
					type="button"
					class="line-through hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.strikethroughText(textArea);
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}
					>S
				</button>
				<button
					type="button"
					class="material-symbols-outlined hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.listText(textArea);
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}>list</button
				>
				<button
					type="button"
					class="material-symbols-outlined hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.listText(textArea, 'ORDERED');
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}
					>format_list_numbered
				</button>
				<button
					type="button"
					class="material-symbols-outlined hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.listText(textArea, 'QUOTE');
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}
					>format_quote
				</button>
				<button
					type="button"
					class="material-symbols-outlined hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.insertTable(textArea);
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}
					>table
				</button>
				<button
					type="button"
					class="material-symbols-outlined hover:bg-black hover:text-white rounded-md size-8"
					onclick={() => {
						markdown.urlText(textArea);
						content = textArea.value; // Update here because changing text through js doesn't update the bound value
					}}
					>link
				</button>
			</div>
		{/if}
	</div>
	{#if preview}
		<div class="w-full bg-black max-h-40 text-white p-4 markdownDescription">
			{#await markdown.MdtoHTML(content) then render}
				{@html render}
			{/await}
		</div>
	{:else}
		<div>
			<textarea
				class="w-full resize-none h-60 outline-none p-3 text-white bg-black font-mono"
				bind:value={content}
				bind:this={textArea}
			></textarea>
		</div>
	{/if}
</div>
