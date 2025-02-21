<script lang="ts">
	import type { PageData } from './$types';
	import SculptureConfig from '$lib/components/input/SculptureConfig.svelte';
	import SortableList from '$lib/components/input/SortableList.svelte';
	import Sortable, { type Options } from 'sortablejs';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';
	import { isEqual } from 'lodash-es';

	const { data }: { data: PageData } = $props();
	const sculptures = data.sculptures;

	let originalOrder: string[] = $state(
		sculptures.map((x: { sculptureData: { id: number } }) => x.sculptureData.id.toString())
	);
	// svelte-ignore state_referenced_locally
	let updatedElements: string[] = $state($state.snapshot(originalOrder));

	let saveDisabled: boolean = $derived(isEqual(updatedElements, originalOrder));

	const sortableOptions: Options = {
		handle: '.handle',
		draggable: '.sculpture',
		chosenClass: 'sculpture-chosen',
		ghostClass: 'sculpture-ghost',
		animation: 150,
		dataIdAttr: 'data-sculptureId',
		onEnd: () => (updatedElements = sortable!.toArray())
	};

	let sortable: Sortable | undefined = $state();

	async function updateOrder() {
		const valuesToUpdate = getArrayDifference(originalOrder, updatedElements);

		const query = `
			mutation updateSculptureIndices($id: Int!, $index: Int!) {
				updateSculptureData(id: $id, index: $index) {
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

<div class="flex flex-col py-3 md:p-3 gap-5 lg:h-[calc(100svh-5rem)] bg-black overflow-clip">
	<h1 class="text-xl text-white text-center">Esculturas</h1>
	<div class="h-full flex-col justify-center items-center w-full max-w-5xl mx-auto">
		<SortableList sortableId="sculpturesList" {sortableOptions} bind:sortable>
			<div id="sculpturesList" class="bg-gray-500 overflow-y-scroll h-4/5">
				{#each sculptures as sculpture (sculpture.filename)}
					<div
						class="sculpture flex border-2 border-black h-1/2"
						data-sculptureId={sculpture.sculptureData.id}
					>
						<span
							class="handle material-symbols-outlined p-2 border-r-2 handle content-center my-2"
						>
							drag_indicator
						</span>
						<SculptureConfig
							filename={sculpture.filename}
							altText={sculpture.altText}
							spaceId={sculpture.space.id}
							projectId={sculpture.space.project.id}
							sculptureData={sculpture.sculptureData}
						/>
					</div>
				{/each}
			</div>
			<div class="flex w-full bg-gray-500">
				<button
					type="button"
					class="w-full border-2 border-black disabled:bg-gray-300 disabled:cursor-not-allowed"
					disabled={saveDisabled}
					onclick={updateOrder}>Actualizar orden</button
				>
				<button
					type="button"
					class="w-full border-2 border-black disabled:bg-gray-300 disabled:cursor-not-allowed"
					disabled={saveDisabled}
					onclick={() => {
						sortable?.sort(originalOrder, true);
						updatedElements = sortable!.toArray();
					}}>Cancelar</button
				>
			</div>
		</SortableList>
	</div>
</div>
