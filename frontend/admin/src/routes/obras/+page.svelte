<script lang="ts">
	import graphql from '$lib/utilities/api';
	import SortableList from '$lib/components/input/SortableList.svelte';
	import Sortable, { type Options } from 'sortablejs';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import { success } from '$lib/utilities/toasts';
	import type { PageData } from './$types';
	import { isEqual, toArray } from 'lodash-es';

	const { data }: { data: PageData } = $props();
	const projects: any[] = data.projects;

	let sortable: Sortable | undefined = $state();
	let originalOrder: string[] = $state(projects.map((x) => x.id.toString()));
	// svelte-ignore state_referenced_locally
	let updatedOrder: string[] = $state($state.snapshot(originalOrder));
	let saveDisabled: boolean = $derived(isEqual(updatedOrder, originalOrder));

	const sortableOptions: Options = {
		draggable: '.item',
		chosenClass: 'item-chosen',
		ghostClass: 'item-ghost',
		animation: 150,
		dataIdAttr: 'data-projectId',
		onEnd: () => (updatedOrder = sortable?.toArray()!),
		delay: 200,
		delayOnTouchOnly: true
	};

	async function updateOrder() {
		const query = `
				mutation UpdateIndex($id: Int!, $index: Int!) {
					updateProject(id: $id, index: $index) {
						id
					}
				}			
		`;

		const newOrder = sortable?.toArray()!;

		const updates = getArrayDifference(originalOrder!, newOrder);

		updates.forEach(
			async ({ id, newPos }) => await graphql(query, { id: parseInt(id), index: newPos })
		);

		originalOrder = newOrder;

		success('Orden actualizado con éxito.');
	}
</script>

<div class="bg-black min-h-screen flex items-center justify-center flex-col gap-5">
	<SortableList bind:sortable {sortableOptions} sortableId="sortable">
		<div class="flex-wrap items-center justify-center w-full lg:flex" id="sortable">
			{#each projects as project, i (project.id)}
				<div
					class={`mx-auto md:mx-0 item flex basis-1/3 ${i <= 2 ? 'h-[calc(100svh-6rem)]' : 'h-screen'} w-fit flex-col justify-center self-center justify-self-center`}
					data-projectId={project.id}
				>
					<a
						href={`/obras/${project.id}`}
						class="m-auto w-fit flex h-2/3 flex-col items-start gap-y-2 transition-transform hover:scale-110"
					>
						<img
							src={project.thumbnail.imageUrl}
							alt={project.thumbnail.altTextEs}
							class="h-full"
						/>
						<p class="font-Agency-FB ml-2 text-xl text-white">{project.name}</p>
					</a>
				</div>
			{/each}
			<a
				id="new-project"
				href="obras/crear"
				class="block p-3 mx-auto md:mx-0 size-20 text-red font-bold text-red-400 hover:bg-vector-grey transition-colors rounded-md"
			>
				<span
					class="material-symbols-outlined size-full md:size-full text-center content-center text-4xl!"
				>
					add
				</span>
			</a>
		</div>
	</SortableList>
	{#if projects.length > 0}
		<div class="flex w-full mb-10 max-w-md border-2 border-black rounded-xs">
			<button
				type="button"
				onclick={updateOrder}
				disabled={saveDisabled}
				class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-r-2"
				>Guardar nuevo orden
			</button>
			<button
				type="button"
				onclick={() => {
					sortable?.sort(originalOrder, true);
					updatedOrder = sortable?.toArray()!;

					// Move the add symbol to the end since it gets sorted alongside everything
					const add = sortable?.el.querySelector('#new-project');
					sortable?.el.appendChild(add!);
				}}
				disabled={saveDisabled}
				class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-l-2"
				>Cancelar
			</button>
		</div>
	{/if}
</div>
