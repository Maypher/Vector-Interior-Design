<script lang="ts">
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { spaceCreateSchema } from '$lib/utilities/yupSchemas';
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { success } from '$lib/utilities/toasts';
	import graphql from '$lib/utilities/api';
	import confirmationDialog from '$lib/utilities/dialog';
	import { goto } from '$app/navigation';
	import { error } from '@sveltejs/kit';
	import { PUBLIC_imageURL } from '$env/static/public';
	import SortableList from '$lib/components/input/SortableList.svelte';
	import Sortable, { type Options } from 'sortablejs';
	import getArrayDifference from '$lib/utilities/arrayOrder';

	const { data }: { data: PageData } = $props();
	let space = $state(data.spaceData);
	let submitting: boolean = $state(false);
	let originalOrder: string[] = $state(
		space.images.map((image: { filename: string }) => image.filename)
	);
	// svelte-ignore state_referenced_locally
	let updatedElements: string[] = $state($state.snapshot(originalOrder));
	let saveDisabled = $derived(updatedElements.toString() === originalOrder.toString());

	let sortable: Sortable | undefined = $state();

	const sortableOptions: Options = {
		draggable: '.image',
		chosenClass: 'image-chosen',
		ghostClass: 'image-ghost',
		animation: 150,
		dataIdAttr: 'data-imageFilename',
		onEnd: () => (updatedElements = sortable!.toArray())
	};

	const { form, errors, enhance, constraints } = superForm(data.updateForm, {
		SPA: true,
		validators: yup(spaceCreateSchema),
		resetForm: false,
		invalidateAll: false,
		async onUpdate({ form: updateForm }) {
			submitting = true;
			if (updateForm.valid) {
				const query = `
                    mutation updateSpace($id: Int!, $name: String, $description: String) {
                        updateSpace(id: $id, name: $name, description: $description) {
                            name
                            description
                        }
                    }
                `;

				const variables = { id: space.id, ...updateForm.data };

				const updatedSpace = (await graphql(query, variables)).updateSpace;
				$form.name = updatedSpace.name;
				$form.description = updatedSpace.description;

				success(`Ambiente "${updatedSpace.name}" actualizado con éxito.`);
			}
			submitting = false;
		}
	});

	async function deleteSpace() {
		if (
			await confirmationDialog(
				`Seguro que quieres borrar el ambiente <b>${space.name}</b> 
				de la obra <b>${space.project.name}</b>? 
				Esta acción no puede ser revertida.`
			)
		) {
			const query = `
				mutation deleteSpace($id: Int!) {
					deleteSpace(id: $id)
				}
			`;

			const variables = { id: space.id };

			const deletedAmbiente = (await graphql(query, variables)).deleteSpace;

			if (deletedAmbiente) {
				await goto(`/obras/${space.project.id}/`);
			} else error(404, `Ambiente con ID ${space.id} no existe.`);
		}
	}

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

<div class="w-full bg-green-300 min-h-screen p-3">
	<form action="POST" use:enhance class="max-w-xl p-3 rounded-md m-auto bg-red-700">
		<fieldset disabled={submitting}>
			<button
				type="button"
				class="block w-fit ml-auto p-2 rounded-sm bg-blue-600 hover:bg-amber-600"
				onclick={deleteSpace}>Eliminar</button
			>
			<EditableInput
				name="nombre"
				label="Nombre"
				type="text"
				bind:value={$form.name}
				errors={$errors.name}
				{...$constraints.name}
			/>
			<Markdown
				label="Descripción"
				name="descripcion"
				bind:value={$form.description}
				errors={$errors.description}
			/>
			<button type="submit" class="bg-violet-300 hover:bg-stone-50 m-2 rounded-sm p-3"
				>Actualizar</button
			>
		</fieldset>
	</form>
	<hr class="m-2 border-blue-700" />
	<div class="m-auto my-10 max-w-5xl w-fit">
		<h1 class="text-xl text-center mb-4">Imágenes</h1>
		<SortableList bind:sortable sortableId="imageSort" {sortableOptions}>
			<div id="imageSort" class="bg-gray-600 rounded-t-md p-5 flex gap-3">
				{#each space.images as image, i (image.filename)}
					<div class="image h-32 relative" data-imageFilename={image.filename}>
						<a href={`/obras/${space.project.id}/ambientes/${space.id}/imagenes/${image.filename}`}>
							<p class="absolute top-0 left-0 bg-white opacity-70 p-2 rounded-br-md">{i + 1}</p>
							<div class="absolute top-0 right-0 flex flex-col bg-white opacity-70 rounded-bl-md">
								{#if space.project.thumbnail?.filename === image.filename}
									<span class="material-symbols-outlined" title="Imagen Principal"> favorite </span>
								{/if}
								{#if image.mainPage}
									<span
										class="material-symbols-outlined"
										title="Esta imagen aparece en la página principal"
									>
										home
									</span>
								{/if}
							</div>
							<img src={`${PUBLIC_imageURL}${image.filename}`} alt={image.altText} class="h-full" />
						</a>
					</div>
				{/each}
			</div>
		</SortableList>
		<div class="flex w-full border-2 border-black rounded-sm">
			<button
				type="button"
				onclick={updateImagesOrder}
				disabled={saveDisabled}
				class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-r-2"
				>Guardar nuevo orden</button
			>
			<button
				type="button"
				onclick={() => {
					sortable?.sort(originalOrder!);
					updatedElements = originalOrder;
				}}
				disabled={saveDisabled}
				class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-l-2"
				>Cancelar</button
			>
		</div>
		<a
			href={`/obras/${space.project.id}/ambientes/${space.id}/imagenes/crear/`}
			class="block w-full text-center m-auto bg-amber-400 hover:bg-white p-2 border-2 border-black"
			>Nueva imagen</a
		>
	</div>
</div>
