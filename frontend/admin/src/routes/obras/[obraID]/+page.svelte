<script lang="ts">
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
	import ImageGrid from '$lib/components/layout/imageGrid.svelte';

	import getArrayDifference from '$lib/utilities/arrayOrder';
	import EditorLinks from '$lib/components/layout/editorLinks.svelte';

	const { data }: { data: PageData } = $props();
	let projectData = $state(data.projectData!);
	let originalSpaceNames: string[] = $state(projectData.spaces.map((space: any) => space.name));
	let submitting: boolean = $state(false);
	let englishDesc: boolean = $state(false);

	let sortable: Sortable | undefined = $state();
	let originalOrder: string[] = $state(projectData.spaces.map((x: { id: string }) => x.id));
	// svelte-ignore state_referenced_locally
	let updatedElements: string[] = $state($state.snapshot(originalOrder));
	let saveDisabled = $derived(updatedElements.toString() === originalOrder.toString());

	const sortableOptions: Options = {
		handle: '.handle',
		draggable: '.item',
		chosenClass: 'item-chosen',
		ghostClass: 'item-ghost',
		animation: 150,
		dataIdAttr: 'data-spaceId',
		onEnd: () => (updatedElements = sortable!.toArray())
	};

	const { form, errors, enhance, constraints } = superForm(data.updateForm!, {
		SPA: true,
		validators: yup(projectCreateSchema), // Uses projectCreateScheme since this will only update name, description and area. All others will be dedicated pages.
		resetForm: false,
		async onUpdate({ form: updateForm }) {
			if (updateForm.valid) {
				const query = `
					mutation updateProject($id: Int!, $name: String, $descriptionEs: String, $descriptionEn: String, $area: Int) {
						updateProject(id: $id, name: $name, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, area: $area) {
							name
							descriptionEs
							descriptionEn
							area
						}
					}
				`;
				const variables = {
					id: projectData.id,
					name: updateForm.data.name,
					descriptionEs: updateForm.data.descriptionEs,
					descriptionEn: updateForm.data.descriptionEn,
					area: updateForm.data.area
				};

				const updateProject = (await graphql(query, variables)).updateProject;
				$form.name = updateProject.name;
				$form.descriptionEs = updateProject.descriptionEs;
				$form.descriptionEn = updateProject.descriptionEn;
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

	async function deleteSpace(space: any) {
		if (
			await confirmationDialog(
				`Seguro que quieres borrar el ambiente <b>${space.name}</b> 
				de del proyecto <b>${projectData.name}</b>? 
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
				window.location.reload();
			} else error(404, `Ambiente con ID ${space.id} no existe.`);
		}
	}

	async function updateSpace(space: any, spaceIndex: number) {
		const query = `
			mutation updateSpace($id: Int!, $name: String) {
				updateSpace(id: $id, name: $name) {
					name
				}
			}
		`;

		const updatedName = (await graphql(query, { id: space.id, name: space.name })).updateSpace.name;

		// Doing it this way since the input are handled inside an {#each} block and I can access the index.
		// Otherwise I'd have to filter the array and what a hassle.
		originalSpaceNames[spaceIndex] = updatedName;

		success(`Espacio ${updatedName} actualizado con éxito.`);
	}
</script>

<div class="bg-vector-black py-5 lg:flex gap-x-10 lg:px-10 overflow-y-hidden lg:header-screen">
	<!-- Name, area and description -->
	<form
		class="bg-vector-cream/50 p-4 lg:rounded-lg flex flex-col justify-stretch gap-y-20 lg:gap-y-10"
		use:enhance
	>
		<div class="flex justify-between">
			<button
				type="button"
				class={`${projectData.public ? 'bg-vector-black text-vector-cream' : 'bg-vector-cream text-black'} brightness-80 hover:brightness-100 p-2 transition-all cursor-pointer rounded-md`}
				onclick={changeProjectStatus}>{projectData.public ? 'Privatizar' : 'Publicar'}</button
			>
			<button
				type="button"
				class="p-2 bg-red-500 hover:brightness-80 cursor-pointer transition-all rounded-md"
				onclick={deleteProject}>Borrar Proyecto</button
			>
		</div>
		<fieldset
			disabled={submitting}
			class="grow flex flex-col gap-y-20 lg:gap-y-0 justify-between items-start"
		>
			<div class="text-3xl">
				<div class="w-1/2 flex items-center input-container">
					<input
						type="text"
						id="project-name"
						class="outline-0 font-Agency-FB"
						bind:value={$form.name}
					/>
					<label for="project-name" class="material-symbols-outlined"> edit </label>
				</div>
				<div class="h-0.5 w-full bg-vector-grey input-underline"></div>
			</div>
			<div class="text-2xl flex gap-2">
				<label for="project-area">Área(m²):</label>
				<div>
					<div class="w-1/2 flex items-center input-container">
						<input
							type="number"
							id="project-area"
							min="0"
							class="outline-0 font-Agency-FB w-15"
							bind:value={$form.area}
						/>
					</div>
					<div class="h-0.5 w-full bg-vector-grey input-underline"></div>
				</div>
			</div>
			<div class="w-full">
				<div class="flex gap-2 items-center mb-2">
					<label for="description" class="block mb-2 text-2xl">Descripción</label>
					<label for="en-desc" class="bg-vector-orange border-2 border-black p-1"
						>{englishDesc ? 'Ingles' : 'Español'}</label
					>
					<input type="checkbox" id="en-desc" hidden bind:checked={englishDesc} />
				</div>
				{#if englishDesc}
					<textarea
						id="description"
						bind:value={$form.descriptionEn}
						class="border-2 border-dashed w-full p-2 min-h-40 max-h-50 font-mono bg-gray-700/70 text-white"
					></textarea>
				{:else}
					<textarea
						id="description"
						bind:value={$form.descriptionEs}
						class="border-2 border-dashed w-full p-2 min-h-40 max-h-50 font-mono bg-gray-700/70 text-white"
					></textarea>
				{/if}
			</div>
			<button
				class="bg-vector-cream hover:brightness-75 transition-colors p-1 rounded-md cursor-pointer"
				>Actualizar
			</button>
		</fieldset>
	</form>
	<div class="grow flex h-full flex-col justify-between">
		<!-- Ambientes -->
		<div class="h-full my-10 lg:my-0">
			<h1 class="text-xl m-3 mt-0 font-bold text-center text-white">Ambientes</h1>
			<div class="max-h-9/10 overflow-y-scroll">
				<SortableList bind:sortable sortableId="sortable" {sortableOptions}>
					<div id="sortable" class="overflow-y-scroll h-full">
						{#each projectData.spaces as space, i (space.id)}
							{@const radioId = `${space.id}-collapse`}
							<div class="item bg-gray-600 border-2 border-black" data-spaceId={space.id}>
								<div class="space-header h-10 flex items-center" data-ambienteId={space.id}>
									<span
										class="material-symbols-outlined handle p-2 h-fit content-center hover:cursor-pointer self-start"
									>
										drag_indicator
									</span>
									<div
										class="cursor-pointer size-full pl-2 flex justify-between items-center transition-colors from-transparent to-transparent bg-gradient-to-r from-0% hover:from-transparent hover:to-vector-orange text-white"
									>
										<div class="flex items-center gap-2">
											<input type="text" id={`${space.id}-name`} bind:value={space.name} />
											<label for={`${space.id}-name`} class="cursor-pointer">
												<span class="material-symbols-outlined"> edit </span>
											</label>
											<button
												type="button"
												class="cursor-pointer transition-all text-green-500 hover:text-green-700"
												class:opacity-0={originalSpaceNames[i] === space.name}
												onclick={() => updateSpace(space, i)}
											>
												<span class="material-symbols-outlined"> check </span>
											</button>
										</div>
										<button
											class="grow flex justify-end cursor-pointer"
											onclick={() => {
												const radioBtn = document.getElementById(radioId) as HTMLInputElement;
												radioBtn.checked = !radioBtn.checked;
											}}
										>
											<span class="mx-2 arrow transition-transform">&lt;</span>
										</button>
									</div>
									<input type="radio" name="space-images" id={radioId} hidden />
									<button
										class="ml-2 p-2 cursor-pointer hover:bg-red-500 hover:text-black transition-colors font-bold text-red-500"
										onclick={() => deleteSpace(space)}
										>X
									</button>
								</div>
								<div class="grid images-wrapper transition-all overflow-hidden bg-gray-800">
									<ImageGrid projectId={projectData.id} spaceId={space.id} images={space.images} />
								</div>
							</div>
						{/each}
					</div>
				</SortableList>
				<div class="sticky bottom-0">
					<div class="flex w-full border-2 border-black rounded-xs">
						<button
							type="button"
							onclick={updateOrder}
							disabled={saveDisabled}
							class="w-full cursor-pointer bg-blue-300 p-1 disabled:bg-gray-800 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-r-2"
							>Guardar nuevo orden
						</button>
						<button
							type="button"
							onclick={() => {
								sortable?.sort(originalOrder!, true);
								updatedElements = $state.snapshot(originalOrder);
							}}
							disabled={saveDisabled}
							class="w-full cursor-pointer bg-blue-300 p-1 disabled:bg-gray-800 disabled:text-gray-400 hover:bg-gray-200 transition-colors disabled:cursor-not-allowed border-l-2"
							>Cancelar
						</button>
					</div>
					<a
						href={`/obras/${projectData.id}/ambientes/crear/`}
						class="block transition-colors bg-amber-400 hover:bg-amber-600 w-full text-center p-2 border-2 border-black"
						>Nuevo Ambiente
					</a>
				</div>
			</div>
		</div>
		<div class="mx-auto">
			<EditorLinks
				mobileUrl={`/obras/${projectData.id}/movil`}
				desktopUrl={`/obras/${projectData.id}/escritorio`}
			/>
		</div>
	</div>
</div>

<style>
	.images-wrapper {
		grid-template-rows: 0fr;
	}

	.space-header:has(input[type='radio']:checked) + .images-wrapper {
		padding: 0.5rem;
		grid-template-rows: 1fr;
	}

	.space-header:has(input[type='radio']:checked) .arrow {
		transform: rotate(-90deg);
	}

	.input-underline {
		background: linear-gradient(
			to right,
			var(--color-vector-orange) 50%,
			var(--color-vector-grey) 50%
		);
		background-size: 200%;
		background-position: right;
		transition: background-position 0.3s ease-out;
	}

	.input-container:has(input:focus) + .input-underline {
		background-position: left;
	}
</style>
