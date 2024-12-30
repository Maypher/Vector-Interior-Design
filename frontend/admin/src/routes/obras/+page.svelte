<script lang="ts">
	import { untrack } from 'svelte';
	import graphql from '$lib/utilities/api';
	import { PUBLIC_imageURL } from '$env/static/public';
	import SortableList from '$lib/components/input/SortableList.svelte';
	import Sortable, { type Options } from 'sortablejs';
	import '$lib/styles/ordenableList.css';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import { success } from '$lib/utilities/toasts';

	let searchParams = $state({
		name: '',
		page: 1
	});

	// Used to highlight the search string in the results. Not derived because it should only update on search.
	let nameRegex: RegExp = $derived(new RegExp(`(${searchParams.name})`, 'gi'));

	let obraPromise: Promise<any> | undefined = $derived.by(() => fetchObras());

	let sortable: Sortable | undefined = $state();
	let sortableEnabled: boolean = $derived(searchParams.name === '');
	let originalOrder: string[] | undefined = $state();
	let updatedElements: string[] = $state([]);
	let saveDisabled = $derived(
		!originalOrder ||
			updatedElements.length === 0 ||
			originalOrder?.toString() === updatedElements?.toString()
	);

	$effect(() => {
		const searchQuery = searchParams;
		untrack(() => {
			sortable?.option('disabled', searchQuery.name !== '');
		});
	});

	const sortableOptions: Options = {
		handle: '.handle',
		draggable: '.item',
		chosenClass: 'item-chosen',
		ghostClass: 'item-ghost',
		animation: 150,
		dataIdAttr: 'data-obraId',
		onEnd: () => (updatedElements = sortable!.toArray())
	};

	async function fetchObras() {
		const query = `
			query GetObras($page: Int, $name: String) {
				obras(page: $page, name: $name) {
					page
					pageCount
					obras {
						id
						name
						public
						thumbnail {
							filename
							altText
						}
					}
				}
			}	
		`;
		const obras = (await graphql(query, searchParams)).obras;

		// Due to how the structure is setup this makes sure the original order is only set on first load.
		// To later compare it and only update those values that were moved.
		if (!originalOrder) {
			originalOrder = obras.obras.map(({ id }: { id: number }) => id.toString());
		}

		return (await graphql(query, searchParams)).obras;
	}

	async function updateOrder() {
		const query = `
				mutation UpdateIndex($id: Int!, $index: Int!) {
					updateObra(id: $id, index: $index) {
						id
					}
				}			
		`;

		const updates = getArrayDifference(originalOrder!, updatedElements);

		updates.forEach(
			async ({ id, newPos }) => await graphql(query, { id: parseInt(id), index: newPos })
		);

		originalOrder = updatedElements;

		success('Orden actualizado con éxito.');
	}
</script>

<div class="bg-red-400 min-h-screen p-4">
	<div class="bg-gray-500 p-2 flex justify-between items-center rounded-lg max-w-md m-auto">
		<input type="text" class="bg-transparent outline-none w-full" bind:value={searchParams.name} />
		<span class="material-symbols-outlined border-l-2 border-gray-700 pl-3"> search </span>
	</div>
	<div class="my-4 max-w-md m-auto">
		{#if obraPromise}
			{#await obraPromise}
				<p>Cargando...</p>
			{:then data}
				{#if data.obras.length == 0}
					{`Ninguna obra encontrada.`}
				{:else}
					<SortableList bind:sortable {sortableOptions} sortableId="sortable">
						<div id="sortable">
							{#each data.obras as obra (obra.id)}
								<div
									class="item flex items-center"
									class:!bg-red-300={!obra.public}
									data-obraId={obra.id}
								>
									{#if sortableEnabled}
										<span
											class="material-symbols-outlined handle border-r-2 p-2 h-full content-center border-gray-800 hover:cursor-pointer"
										>
											drag_indicator
										</span>
									{/if}
									<a
										href={`/obras/${obra.id}`}
										class={`size-full flex justify-between items-center pl-2 ${!obra.public ? 'hover:bg-red-400' : 'hover:bg-amber-600'}`}
									>
										<div class="flex gap-2 items-center">
											{#if !obra.public}
												<span
													class="material-symbols-outlined text-red-500"
													title="Esta obra es privada. No será visible al público"
												>
													visibility_off
												</span>
											{/if}
											<p>
												{@html obra.name.replace(nameRegex, '<b>$1</b>')}
											</p>
										</div>
										{#if obra.thumbnail}
											<img
												src={`${PUBLIC_imageURL}${obra.thumbnail?.filename}`}
												alt={obra.thumbnail?.altText}
												class="max-h-full"
											/>
										{/if}
									</a>
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
							onclick={() => sortable?.sort(originalOrder!)}
							disabled={saveDisabled}
							class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-l-2"
							>Cancelar</button
						>
					</div>
					<a
						href="/obras/crear"
						class="block bg-amber-400 hover:bg-amber-600 w-full text-center p-2 border-2 border-black sticky bottom-0"
						>Nueva Obra</a
					>
				{/if}
				<div class="flex gap-3 w-fit m-auto my-2 text-lg items-center">
					{#if searchParams.page > 1}
						<button
							class="rounded-lg p-1 hover:font-bold hover:bg-gray-300"
							onclick={() => {
								searchParams.page--;
							}}>&lt</button
						>
					{/if}
					<p>{data.page}/{data.pageCount}</p>
					{#if searchParams.page < data.pageCount}
						<button
							class="rounded-lg p-1 hover:font-bold hover:bg-gray-300"
							onclick={() => searchParams.page++}
							>&gt
						</button>
					{/if}
				</div>
			{/await}
		{/if}
	</div>
</div>
