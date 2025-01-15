<script lang="ts">
	import type { PageData } from './$types';
	import SculptureConfig from '$lib/components/input/SculptureConfig.svelte';
	import SortableList from '$lib/components/input/SortableList.svelte';
	import Sortable, { type Options } from 'sortablejs';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	const sculptures = data.sculptures;

	let originalOrder: string[] = $state(
		sculptures.map((x: { sculptureData: { id: number } }) => x.sculptureData.id.toString())
	);
	// svelte-ignore state_referenced_locally
	let updatedElements: string[] = $state($state.snapshot(originalOrder));

	let saveDisabled: boolean = $derived(updatedElements.every((val, i) => originalOrder[i] === val));

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

<h1 class="text-xl m-5 text-center">Esculturas</h1>
<div class="flex flex-col justify-center items-center min-h-screen">
	<div>
		<SortableList sortableId="sculpturesList" {sortableOptions} bind:sortable>
			<div id="sculpturesList" class="bg-gray-500 max-h-[39rem] overflow-y-scroll">
				{#each sculptures as sculpture (sculpture.filename)}
					<div
						class="sculpture flex border-2 border-black"
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
			<div class="flex bg-gray-500">
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
					onclick={() => (updatedElements = originalOrder)}>Cancelar</button
				>
			</div>
		</SortableList>
	</div>
</div>
