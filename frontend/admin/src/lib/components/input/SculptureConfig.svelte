<script lang="ts">
	import { PUBLIC_imageURL } from '$env/static/public';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';
	import Markdown from '../markdown/Markdown.svelte';

	interface SculptureData {
		id: number;
		descriptionEs: string;
		descriptionEn: string;
	}

	interface Props {
		filename: string;
		altText: string;
		sculptureData: SculptureData;
		spaceId: number;
		projectId: number;
	}

	const { filename, altText, sculptureData, spaceId, projectId }: Props = $props();

	const dataClone = $state.snapshot(sculptureData);
	let originalData = $state(dataClone);
	let updatedData = $state(dataClone);
	let shouldUpdate = $derived(JSON.stringify(originalData) !== JSON.stringify(updatedData));

	let englishDesc: boolean = $state(false);

	async function onsubmit(e: SubmitEvent) {
		e.preventDefault();

		const query = `
            mutation updateSculptureData($id: Int!, $descriptionEs: String, $descriptionEn: String) {
                updateSculptureData(id: $id, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn) {
					id
                    descriptionEn
                    descriptionEs
                }
            }
        `;

		const updateSculptureData = (await graphql(query, updatedData)).updateSculptureData;

		success('Información de escultura actualizada correctamente.');

		updatedData = updateSculptureData;
		originalData = updateSculptureData;
	}
</script>

<form {onsubmit} class="flex w-full items-center p-3 gap-4">
	<a href={`/obras/${projectId}/ambientes/${spaceId}/imagenes/${filename}`}>
		<img src={`${PUBLIC_imageURL}${filename}`} alt={altText} class="h-64" />
	</a>
	<div>
		<div class="flex">
			<button
				type="button"
				class="w-full border-black border-2 hover:bg-red-500"
				class:bg-red-200={!englishDesc}
				onclick={() => (englishDesc = false)}>Español</button
			>
			<button
				type="button"
				class="w-full border-black border-2 hover:bg-red-500"
				class:bg-red-200={englishDesc}
				onclick={() => (englishDesc = true)}>Ingles</button
			>
		</div>
		{#if !englishDesc}
			<Markdown
				label="Descripción Español"
				name="description_es"
				errors={[]}
				bind:value={updatedData.descriptionEs}
			/>
		{:else}
			<Markdown
				label="Descripción Ingles"
				name="description_en"
				errors={[]}
				bind:value={updatedData.descriptionEn}
			/>
		{/if}
	</div>
	<div
		class="overflow-hidden transition-all flex flex-col h-full justify-center gap-10"
		class:w-0={!shouldUpdate}
		class:w-fit={shouldUpdate}
	>
		<button
			type="submit"
			class="text-green-200 bg-black p-1 rounded-md hover:bg-blue-900 transition-all"
			><span class="material-symbols-outlined"> check </span></button
		>
		<button
			type="button"
			class="text-red-200 bg-black p-1 rounded-md hover:bg-blue-900 transition-all"
			onclick={() => (updatedData = dataClone)}
			><span class="material-symbols-outlined content-center h-full"> close </span></button
		>
	</div>
</form>
