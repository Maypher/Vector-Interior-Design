<script lang="ts">
	import Sortable, { type Options } from 'sortablejs';
	import SortableList from '../input/SortableList.svelte';
	import { isEqual } from 'lodash-es';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';

	interface Props {
		projectId: number;
		spaceId: number;
		images: any[];
	}

	const { projectId, spaceId, images }: Props = $props();

	let originalOrder = $state(images.map((x: any) => x.filename));
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
			mutation updateImage($filename: String!, $index: Int!) {
				updateImage(filename: $filename, index: $index) {
					filename
				}
			}
		`;

		const updates = getArrayDifference(originalOrder, updatedElements);

		updates.forEach(async ({ id, newPos }) => {
			await graphql(query, { filename: id, index: newPos });
		});

		originalOrder = updatedElements;

		success('Orden actualizado con éxito.');
	}
</script>

<SortableList bind:sortable sortableId={`sortable-${spaceId}`} {sortableOptions}>
	<div
		id={`sortable-${spaceId}`}
		class="grid grid-cols-3 lg:grid-cols-5 gap-5 items-center w-full overflow-y-scroll overflow-x-hidden images-container"
	>
		{#each images as image (image.filename)}
			<a
				href={`/obras/${projectId}/ambientes/${spaceId}/imagenes/${image.filename}`}
				class="image-item transition-all border-vector-orange hover:border-4 relative"
				data-imageId={image.filename}
			>
				<img src={image.imageUrl} alt={image.altTextEs} />
				<div
					class="absolute top-0 left-0 text-yellow-500 bg-vector-black/70 text-2xl px-1 pb-0.5 flex gap-x-2 items-start"
				>
					{#if image.space.project.thumbnail.filename === image.filename}
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
		<a
			id={`new-image-${spaceId}`}
			href={`/obras/${projectId}/ambientes/${spaceId}/imagenes/crear`}
			class="flex items-center justify-center size-1/2 min-h-20 hover:bg-vector-grey transition-colors rounded-md m-auto"
		>
			<span
				class="material-symbols-outlined text-center content-center m-auto text-4xl text-red font-bold text-red-400"
			>
				add
			</span>
		</a>
		<div
			id={`cancel-images-${spaceId}`}
			class={`${saveEnabled ? 'opacity-100' : 'opacity-0'} transition-all flex flex-col items-center gap-1`}
		>
			<button
				class="w-fit text-xl p-1 rounded-md text-green-500 hover:bg-green-500 hover:text-black"
				onclick={updateImagesOrder}
				>✓
			</button>
			<button
				type="button"
				onclick={() => {
					sortable?.sort(originalOrder!);
					updatedElements = originalOrder;

					const add = sortable?.el.querySelector(`#new-image-${spaceId}`);
					const buttons = sortable?.el.querySelector(`#cancel-images-${spaceId}`);

					sortable?.el.appendChild(add!);
					sortable?.el.appendChild(buttons!);
				}}
				class="w-fit text-xl text-red-500 p-1 rounded-md hover:text-black hover:bg-red-500 transition-colors cursor-pointer"
			>
				X
			</button>
		</div>
	</div>
</SortableList>
