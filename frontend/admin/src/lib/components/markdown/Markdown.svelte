<script lang="ts">
	import '$lib/styles/markdown.css';
	import { onMount } from 'svelte';
	import * as markdown from '$lib/utilities/markdown';
	import EditorBtn from './EditorBtn.svelte';
	import Errors from '../input/Errors.svelte';

	interface Props {
		label: string;
		name: string;
		value?: string;
		previewDefault?: boolean;
		fontSize?: number;
		fontFamily?: string;
		fontAlignment?: string;
		errors: Array<string> | undefined;
	}

	let {
		label,
		name,
		value = $bindable(''),
		previewDefault = false,
		fontSize = 1,
		fontFamily = 'Arial',
		fontAlignment = 'text-left',
		errors,
		...constrains
	}: Props = $props();

	let preview: boolean = $state(previewDefault);

	let textArea: HTMLTextAreaElement = $state()!;

	function setPreview(val: boolean) {
		preview = val;
	}

	// Updates a list when Enter is pressed.
	onMount(() => markdown.updateListOnEnter(textArea));
</script>

<div class="w-full max-w-2xl">
	<label for={name} class="block m-2 font-semibold">{label}</label>
	<div class="flex justify-between items-center text-gray-400 bg-gray-700 rounded-t-md">
		<div class="h-12 mx-3 whitespace-nowrap">
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
		<div class={`flex gap-1 items-center mx-2 ${preview ? 'invisible' : 'visible'}`}>
			<EditorBtn
				onclick={() => {
					markdown.boldText(textArea);
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="font-bold">N</span>
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.italicText(textArea);
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="italic">I</span>
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.titleText(textArea);
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				>T
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.strikethroughText(textArea);
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="line-through">S</span>
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.listText(textArea);
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="material-symbols-outlined">list</span>
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.listText(textArea, 'ORDERED');
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="material-symbols-outlined">format_list_numbered</span>
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.listText(textArea, 'QUOTE');
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="material-symbols-outlined">format_quote</span>
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.insertTable(textArea);
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="material-symbols-outlined">table</span>
			</EditorBtn>
			<EditorBtn
				onclick={() => {
					markdown.urlText(textArea);
					value = textArea.value; // Update here because changing text through js doesn't update the bound value
				}}
				><span class="material-symbols-outlined">link</span>
			</EditorBtn>
		</div>
	</div>
	{#if preview}
		<div
			class={`w-full bg-black h-60 outline-hidden text-white p-4 markdownDescription overflow-y-scroll ${fontAlignment}`}
			style={`font-family: ${fontFamily};`}
		>
			{@html markdown.mdToHTML(value)}
		</div>
	{:else}
		<div>
			<textarea
				class="w-full resize-none min-h-60 outline-hidden p-4 text-white bg-black font-mono"
				{name}
				bind:value
				bind:this={textArea}
				{...constrains}
			></textarea>
		</div>
	{/if}
	{#if errors}<Errors {errors} />{/if}
</div>
