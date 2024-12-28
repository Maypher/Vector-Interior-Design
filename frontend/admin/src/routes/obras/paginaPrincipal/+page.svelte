<script lang="ts">
	import { type PageData } from './$types';
	import SortableList from '$lib/components/input/SortableList.svelte';
	import Sortable, { type Options } from 'sortablejs';
	import MainPageImage from '$lib/components/input/MainPageImage.svelte';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	let mainPageImages: any[] = $state(data.mainPageData);
	let originalOrder: string[] = $state(
		mainPageImages.map((x: { mainImageConfig: { id: number } }) => x.mainImageConfig.id.toString())
	);
	// svelte-ignore state_referenced_locally
	let updatedElements: string[] = $state($state.snapshot(originalOrder));

	let saveDisabled: boolean = $derived(updatedElements.every((val, i) => originalOrder[i] === val));

	const sortableOptions: Options = {
		handle: '.handle',
		draggable: '.image',
		chosenClass: 'image-chosen',
		ghostClass: 'image-ghost',
		animation: 150,
		dataIdAttr: 'data-imageId',
		onEnd: () => (updatedElements = sortable!.toArray())
	};

	let sortable: Sortable | undefined = $state();

	async function updateOrder() {
		const valuesToUpdate = getArrayDifference(originalOrder, updatedElements);

		const query = `
			mutation updateMainPageIndices($id: Int!, $index: Int!) {
				updateImageConfig(id: $id, index: $index) {
					id
				}
			}
		`;

		valuesToUpdate.forEach(
			async ({ id, newPos }) => await graphql(query, { id: parseInt(id), index: newPos })
		);

		originalOrder = $state.snapshot(updatedElements);
		success('Orden actualizado correctamente');
	}
</script>

<div class="w-screen min-h-screen bg-green-500 flex flex-col items-center p-10">
	<h1 class="font-bold text-xl my-6">Imágenes en Página Principal</h1>
	<div>
		<SortableList bind:sortable sortableId="mainPageSortable" {sortableOptions}>
			<div id="mainPageSortable" class="bg-gray-500">
				{#each mainPageImages as image (image.filename)}
					<div
						class="image flex items-stretch border-2 border-black"
						data-imageId={image.mainImageConfig.id}
					>
						<span class="material-symbols-outlined p-2 border-r-2 handle content-center my-2">
							drag_indicator
						</span>
						<MainPageImage
							image={{
								filename: image.filename,
								altText: image.altText,
								ambienteId: image.ambiente.id,
								obraId: image.ambiente.obra.id
							}}
							imageConfig={image.mainImageConfig}
						/>
					</div>
				{/each}
			</div>
		</SortableList>
		<div class="flex w-full border-2 border-black rounded-sm">
			<button
				type="button"
				onclick={updateOrder}
				disabled={saveDisabled}
				class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-r-2"
				>Guardar nuevo orden</button
			>
			<button
				type="button"
				onclick={() => {
					sortable?.sort(originalOrder!);
					updatedElements = $state.snapshot(originalOrder);
				}}
				disabled={saveDisabled}
				class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-l-2"
				>Cancelar</button
			>
		</div>
	</div>
</div>
