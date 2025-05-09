<script lang="ts">
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';
	import { cloneDeep, isEqual } from 'lodash-es';
	import BgColor from '../editor/BgColor.svelte';

	interface SculptureData {
		id: number;
		descriptionEs: string;
		descriptionEn: string;
		bgColor: string;
	}

	interface Props {
		imageUrl: string;
		altText: string;
		sculptureData: SculptureData;
		spaceId: number;
		projectId: number;
	}

	let { imageUrl: filename, altText, sculptureData, spaceId, projectId }: Props = $props();

	let originalData = $state.snapshot(sculptureData);
	let updatedData = $state($state.snapshot(sculptureData));
	let shouldUpdate = $derived(!isEqual(originalData, updatedData));

	let englishDesc: boolean = $state(false);

	async function onsubmit(e: SubmitEvent) {
		e.preventDefault();

		const query = `
            mutation updateSculptureData($id: Int!, $descriptionEs: String, $descriptionEn: String, $bgColor: String) {
                updateSculptureData(id: $id, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, bgColor: $bgColor) {
					id
                    descriptionEn
                    descriptionEs
					bgColor
                }
            }
        `;

		const updateSculptureData = (await graphql(query, updatedData)).updateSculptureData;

		success('Información de escultura actualizada correctamente.');

		updatedData = updateSculptureData;
		originalData = updateSculptureData;
	}
</script>

<form
	{onsubmit}
	class="flex flex-col md:flex-row size-full p-3 gap-4 justify-stretch"
	style={`background-color: ${updatedData.bgColor};`}
>
	<a href={`/proyectos/${projectId}/ambientes/${spaceId}/imagenes/${filename}`} class="h-full">
		<img src={filename} alt={altText} class="h-full w-auto" />
	</a>
	<div class="flex w-full gap-2 bg-vector-cream/40 p-1">
		<div class="flex flex-col gap-2 h-full grow">
			<label for="description">Descripción</label>
			<div class="flex bg-vector-cream">
				<button
					type="button"
					class="w-full border-black border-2 hover:bg-vector-orange transition-colors cursor-pointer"
					class:bg-vector-orange={!englishDesc}
					onclick={() => (englishDesc = false)}
					>Español
				</button>
				<button
					type="button"
					class="w-full border-black border-2 hover:bg-vector-orange transition-colors cursor-pointer"
					class:bg-vector-orange={englishDesc}
					onclick={() => (englishDesc = true)}
					>Ingles
				</button>
			</div>
			<div class="flex flex-col gap-2 h-full">
				{#if !englishDesc}
					<textarea
						id="description"
						bind:value={updatedData.descriptionEs}
						class="border-2 border-white border-dashed h-2/3 min-h-50 md:min-h-0 p-2 bg-gray-700 text-white font-mono"
					></textarea>
				{:else}
					<textarea
						id="description"
						bind:value={updatedData.descriptionEn}
						class="border-2 border-white border-dashed h-2/3 min-h-50 md:min-h-0 p-2 bg-gray-700 text-white font-mono"
					></textarea>
				{/if}
			</div>
		</div>
		<div class="self-center size-fit grow-0">
			<BgColor bind:color={updatedData.bgColor} imageId={`${sculptureData.id}`} />
		</div>
		<div
			class={`overflow-hidden transition-all flex md:flex-col grow-0 h-full justify-center gap-10 ${
				shouldUpdate ? 'max-h-200 md:max-w-200' : 'max-h-0 md:max-h-200 md:max-w-0'
			}`}
		>
			<button
				type="submit"
				class="text-green-200 bg-black p-1 rounded-md hover:bg-blue-900 transition-all"
			>
				<span class="material-symbols-outlined"> check </span>
			</button>
			<button
				type="button"
				class="text-red-200 bg-black p-1 rounded-md hover:bg-blue-900 transition-all"
				onclick={() => (updatedData = cloneDeep(originalData))}
			>
				<span class="material-symbols-outlined content-center h-full"> close </span>
			</button>
		</div>
	</div>
</form>
