<script lang="ts">
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { projectCreateSchema } from '$lib/utilities/yupSchemas';
	import { success } from '$lib/utilities/toasts';
	import graphql from '$lib/utilities/api';
	import confirmationDialog from '$lib/utilities/dialog';
	import { goto } from '$app/navigation';
	import { error } from '@sveltejs/kit';
	import SortableList from '$lib/components/input/SortableList.svelte';
	import Sortable, { type Options } from 'sortablejs';
	import '$lib/styles/ordenableList.css';
	import { PUBLIC_imageURL } from '$env/static/public';
	import getArrayDifference from '$lib/utilities/arrayOrder';

	const { data }: { data: PageData } = $props();
	let projectData = $state(data.projectData!);
	let submitting: boolean = $state(false);

	let sortable: Sortable | undefined = $state();
	let originalOrder: string[] = $state(projectData.spaces.map((x: { id: string }) => x.id));
	// svelte-ignore state_referenced_locally
	let updatedElements: string[] = $state(originalOrder);
	let saveDisabled = $derived(updatedElements.toString() === originalOrder.toString());

	const sortableOptions: Options = {
		handle: '.handle',
		draggable: '.item',
		chosenClass: 'item-chosen',
		ghostClass: 'item-ghost',
		animation: 150,
		dataIdAttr: 'data-ambienteId',
		onEnd: () => (updatedElements = sortable!.toArray())
	};

	const { form, errors, enhance, constraints } = superForm(data.updateForm!, {
		SPA: true,
		validators: yup(projectCreateSchema), // Uses projectCreateScheme since this will only update name, description and area. All others will be dedicated pages.
		resetForm: false,
		async onUpdate({ form: updateForm }) {
			if (updateForm.valid) {
				const query = `
					mutation updateProject($id: Int!, $name: String, $description: String, $area: Int) {
						updateProject(id: $id, name: $name, description: $description, area: $area) {
							name
							description
							area
						}
					}
				`;
				const variables = {
					id: projectData.id,
					name: updateForm.data.name,
					description: updateForm.data.description,
					area: updateForm.data.area
				};

				const updateProject = (await graphql(query, variables)).updateProject;
				$form.name = updateProject.name;
				$form.description = updateProject.description;
				$form.area = updateProject.area;

				success(`Proyecto "${updateProject.name}" actualizado con éxito.`);
			}
		}
	});

	async function changeProjectStatus() {
		const query = `
			mutation changePublicStatus($id: Int!, $public: Boolean!) {
				updateProject(id: $id, public: $public) {
					public
				}
			}
		`;

		const variables = { id: projectData.id, public: !projectData.public };

		const updatedPublic = (await graphql(query, variables)).updateProject.public;
		success(updatedPublic ? 'Proyecto publicado con éxito.' : 'Proyecto privatizado con éxito.');
		projectData.public = updatedPublic;
	}

	async function deleteProject() {
		if (
			await confirmationDialog(`Seguro que quieres borrar el proyecto <b>${projectData.name}</b> 
		junto a todos sus ambientes e imágenes?
		Esta acción no puede ser revertida.
		`)
		) {
			const query = `
				mutation deleteProject($id: Int!) {
					deleteProject(id: $id)
				}
			`;

			const variables = { id: projectData.id };

			const deletedProject = (await graphql(query, variables)).deleteProject;

			if (deletedProject) goto('/obras/');
			else error(404, `Proyecto con ID ${projectData.id} no existe.`);
		}
	}

	async function updateOrder() {
		const query = `
				mutation UpdateIndex($id: Int!, $index: Int!) {
					updateSpace(id: $id, index: $index) {
						id
					}
				}			
		`;

		const updates = getArrayDifference(originalOrder, updatedElements);

		updates.forEach(
			async ({ id, newPos }) => await graphql(query, { id: parseInt(id), index: newPos })
		);

		originalOrder = updatedElements;

		success('Orden actualizado con éxito.');
	}
</script>

<div class="bg-green-700 py-20">
	<!-- Name, area and description -->
	<form class="bg-purple-900 m-auto p-4 max-w-xl rounded-lg" use:enhance>
		<button
			type="button"
			class={`${projectData.public ? 'bg-red-500' : 'bg-blue-500'} block w-fit ml-auto p-3 m-3 rounded-md`}
			onclick={changeProjectStatus}>{projectData.public ? 'Privatizar' : 'Publicar'}</button
		>
		<button
			type="button"
			class="block w-fit ml-auto p-3 m-1 bg-red-500 hover:bg-green-600"
			onclick={deleteProject}>Borrar Proyecto</button
		>
		<fieldset disabled={submitting}>
			<EditableInput
				name="name"
				label="Nombre"
				bind:value={$form.name}
				errors={$errors.name}
				type="text"
				{...$constraints.name}
			/>
			<EditableInput
				name="area"
				label="Área (m²)"
				bind:value={$form.area}
				errors={$errors.area}
				type="number"
				{...$constraints.area}
			/>
			<div class="max-w-xl">
				<Markdown
					label="Descripción"
					name="description"
					bind:value={$form.description}
					errors={$errors.description}
					{...$constraints.description}
				/>
			</div>
			<button class="bg-red-400 p-1 m-1 rounded-md">Actualizar</button>
		</fieldset>
	</form>
	<hr class="m-3" />
	<!-- Ambientes -->
	<h1 class="text-xl m-3 font-bold text-center">Ambientes</h1>
	<div class="max-w-md m-auto">
		<SortableList bind:sortable sortableId="sortable" {sortableOptions}>
			<div id="sortable">
				{#each projectData.spaces as space (space.id)}
					<div class="item flex items-center" data-ambienteId={space.id}>
						<span
							class="material-symbols-outlined handle border-r-2 p-2 h-full content-center border-gray-800 hover:cursor-pointer"
						>
							drag_indicator
						</span>
						<div class="size-full">
							<a
								href={`/obras/${projectData.id}/ambientes/${space.id}`}
								class="size-full pl-2 flex justify-between items-center hover:bg-amber-600"
							>
								<p>
									{space.name}
								</p>
								{#if space.images.at(0)}
									<img
										src={`${PUBLIC_imageURL}${space.images[0].filename}`}
										alt={space.images[0].altText}
										class="h-full"
									/>
								{/if}
							</a>
						</div>
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
					updatedElements = originalOrder;
				}}
				disabled={saveDisabled}
				class="w-full bg-blue-300 p-1 disabled:bg-gray-600 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-l-2"
				>Cancelar</button
			>
		</div>
		<a
			href={`/obras/${projectData.id}/ambientes/crear/`}
			class="block bg-amber-400 hover:bg-amber-600 w-full text-center p-2 border-2 border-black sticky bottom-0"
			>Nuevo Ambiente</a
		>
	</div>
</div>
