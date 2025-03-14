<script lang="ts">
	import { TextAlignment, TextFont } from '$lib/utilities/enums';
	import '$lib/styles/markdown.css';
	import { mdToHTML } from '$lib/utilities/markdown';

	interface Props {
		id: string;
		descriptionEs: string;
		descriptionEn?: string;
		descriptionAlignment?: string;
		descriptionFont?: string;
		preview?: boolean;
	}

	let {
		id,
		descriptionEs = $bindable(),
		descriptionEn = $bindable(),
		descriptionAlignment = $bindable(),
		descriptionFont = $bindable(),
		preview = $bindable(false)
	}: Props = $props();

	let englishDescription: boolean = $state(false);
</script>

{#if !preview}
	<div class="flex flex-col justify-between xl:flex-row gap-1">
		{#if descriptionAlignment}
			<div class="flex flex-col items-center">
				<label for={`main-image-desc-alignment-${id}`} class="text-white">Alineación</label>
				<select
					id={`main-image-desc-alignment-${id}`}
					bind:value={descriptionAlignment}
					class="bg-white text-black w-fit m-auto"
				>
					{#each Object.entries(TextAlignment) as [key, val] (key)}
						<option value={val}>{key}</option>
					{/each}
				</select>
			</div>
		{/if}
		{#if descriptionEn !== undefined && descriptionEs !== undefined}
			<div class="flex items-center justify-center">
				<label
					for={`main-image-desc-lang-${id}`}
					class="hover:cursor-pointer bg-vector-cream p-1 rounded-xs hover:brightness-75 transition-colors select-none text-black"
					>{englishDescription ? 'Inglés' : 'Español'}</label
				>
				<input
					type="checkbox"
					id={`main-image-desc-lang-${id}`}
					bind:checked={englishDescription}
					hidden
				/>
			</div>
		{/if}
		{#if descriptionFont}
			<div class="flex flex-col items-center">
				<label for={`main-image-desc-font-${id}`} class="text-white">Tipografía</label>
				<select
					id={`main-image-desc-font-${id}`}
					bind:value={descriptionFont}
					class="bg-white text-black w-fit m-auto"
				>
					{#each Object.entries(TextFont) as [key, val] (key)}
						<option value={val}>{key}</option>
					{/each}
				</select>
			</div>
		{/if}
	</div>
	{#if englishDescription}
		<textarea
			class={`text-white bg-transparent border-2 border-dashed w-full border-white h-44 p-5 ${descriptionAlignment} font-${descriptionFont}`}
			bind:value={descriptionEn}
		></textarea>
	{:else}
		<textarea
			class={`text-white bg-transparent border-2 border-dashed w-full border-white h-44 p-5 ${descriptionAlignment} font-${descriptionFont}`}
			bind:value={descriptionEs}
		></textarea>
	{/if}
{:else}
	<div class={`markdownDescription text-white ${descriptionAlignment} font-${descriptionFont}`}>
		{@html mdToHTML(englishDescription ? descriptionEn! : descriptionEs)}
	</div>
{/if}
