<script lang="ts">
	import Sortable, { type Options } from 'sortablejs';
	import SortableList from '../input/SortableList.svelte';
	import { isEqual } from 'lodash-es';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';

	interface Props {
		images: any[];
	}

	const { images }: Props = $props();

	let originalOrder = $state(images.map((x: any) => `${x.mainImageConfig.id}`));
	// svelte-ignore state_referenced_locally
	let updatedElements = $state($state.snapshot(originalOrder));

	let sortable: Sortable | undefined = $state();
	const sortableOptions: Options = {
		draggable: '.image-item',
		chosenClass: 'item-chosen',
		ghostClass: 'item-ghost',
		animation: 150,
		dataIdAttr: 'data-imageId',
		onEnd: () => (updatedElements = sortable!.toArray())
	};

	let saveEnabled: boolean = $derived(!isEqual(originalOrder, updatedElements));

	async function updateImagesOrder() {
		const query = `
			mutation updateMainPageConfig($id: Int!, $index: Int!) {
				updateMainPageConfig(id: $id, index: $index) {
					id
				}
			}
		`;

		const updates = getArrayDifference(originalOrder, updatedElements);

		updates.forEach(async ({ id, newPos }) => {
			await graphql(query, { id: parseInt(id), index: newPos });
		});

		originalOrder = updatedElements;

		success('Orden actualizado con éxito.');
	}
</script>

<SortableList bind:sortable sortableId="sortable-main-page" {sortableOptions}>
	<div
		id="sortable-main-page"
		class="grid grid-cols-3 lg:grid-cols-5 gap-5 items-center w-full overflow-y-scroll overflow-x-hidden images-container"
	>
		{#each images as image (image.filename)}
			<a
				href={`/proyectos/${image.space.project.id}/ambientes/${image.space.id}/imagenes/${image.filename}`}
				class="image-item transition-all border-vector-orange hover:border-4 relative"
				data-imageId={image.mainImageConfig.id}
			>
				<img src={image.imageUrl} alt={image.altTextEs} />
				<div
					class="absolute top-0 left-0 text-yellow-500 bg-vector-black/70 text-2xl px-1 pb-0.5 flex gap-x-2 items-start"
				>
					{#if image.space.project.thumbnail?.filename === image.filename}
						<div title="Imagen principal">⭐</div>
					{/if}
					{#if image.mainPage}
						<div title="Imagen en página principal">🏠</div>
					{/if}
					{#if image.sculpture}
						<div title="Imagen es una escultura">🖼️</div>
					{/if}
				</div>
			</a>
		{/each}
		<div
			id="cancel-images-main-page"
			class={`${saveEnabled ? 'opacity-100' : 'opacity-0'} transition-all flex flex-col items-center gap-1`}
		>
			<button
				class="w-fit text-xl p-1 rounded-md text-green-500 hover:bg-green-500 hover:text-black"
				onclick={updateImagesOrder}
			>
				✓
			</button>
			<button
				type="button"
				onclick={() => {
					sortable?.sort(originalOrder!);
					updatedElements = originalOrder;

					let buttons = document.getElementById('cancel-images-main-page')!;

					sortable?.el.appendChild(buttons);
				}}
				class="w-fit text-xl text-red-500 p-1 rounded-md hover:text-black hover:bg-red-500 transition-colors cursor-pointer"
			>
				X
			</button>
		</div>
	</div>
</SortableList>
