<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import { yup } from 'sveltekit-superforms/adapters';
	import { createProjectSchema } from '$lib/utilities/yupSchemas';
	import TextInput from '$lib/components/input/TextInput.svelte';
	import { PUBLIC_graphql } from '$env/static/public';
	import { error } from '$lib/utilities/toasts';
	import { goto } from '$app/navigation';
	import Errors from '$lib/components/input/Errors.svelte';

	const { data }: { data: PageData } = $props();
	let inputFile: File | undefined | null = $state();
	let fileErrors: Array<string> = $state([]);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.createForm, {
		SPA: true,
		validators: yup(createProjectSchema),
		async onUpdate({ form: createForm }) {
			fileErrors = [];
			submitting = true;

			if (createForm.valid) {
				if (!inputFile) {
					fileErrors.push('Imagen requerida.');
					submitting = false;
					return;
				}

				if (inputFile.size > 1e7) {
					fileErrors.push('Imagen debe ser menor a 10 Mb.');
					submitting = false;
					return;
				}

				const query = `
                    mutation createImage(
                        $spaceId: Int!,
                        $file: Upload!,
                        $altText: String!
                        ) {
                        createImage(
                            spaceId: $spaceId,
                            image: $file,
                            altText: $altText
                        ) {
                            __typename
                            ... on Image {
                                filename
                            }
                            ... on SpaceNotFoundImage {
                                spaceId
                            }
                            ... on UnsupportedFileType {
                                filetype 
                            }
                        }
                        }
                `;

				const variables = {
					file: null,
					altText: createForm.data.altText,
					spaceId: data.ambienteID
				};

				const operations = JSON.stringify({ query, variables });
				const map = JSON.stringify({ file: ['variables.file'] });

				let formData = new FormData();

				formData.append('operations', operations);
				formData.append('map', map);
				formData.append('file', inputFile);

				const res = await fetch(PUBLIC_graphql, {
					method: 'POST',
					body: formData,
					credentials: 'include'
				});

				if (res.ok) {
					const imageData = (await res.json()).data.createImage;
					console.log(imageData);

					switch (imageData.__typename) {
						case 'AmbienteNotFoundImage':
							error(
								`No se puede registrar la imagen en ambiente con ID ${imageData.ambienteId} porque no existe.`
							);
							break;
						case 'UnsupportedFileType':
							fileErrors.push(`Archivo tipo ${imageData.fileType} no es válido.`);
							break;
						case 'Image':
							await goto(`/obras/${data.obraID}/ambientes/${data.ambienteID}/`);
							break;
					}
				} else if (res.status === 413) {
					fileErrors.push('Imagen debe ser menor a 10 Mb.');
				}
			}

			submitting = false;
		}
	});

	function ondragenter(event: DragEvent) {
		event.preventDefault();
		document.getElementById('dropzone')!.classList.add('hovering');
	}

	function ondragleave(event: DragEvent) {
		event.preventDefault();

		const dropzone = document.getElementById('dropzone')!;
		const childElement = event.relatedTarget;
		// Doing this because it triggers when entering a child element.
		// This way it doesn't remove the class when entering a child element.
		if (childElement && !dropzone.contains(childElement as Node))
			document.getElementById('dropzone')!.classList.remove('hovering');
	}

	function ondrop(event: DragEvent) {
		event.preventDefault();
		document.getElementById('dropzone')!.classList.remove('hovering');

		const file = event.dataTransfer?.files.item(0);
		if (file) inputFile = file;
	}
</script>

<div class="m-5">
	<form use:enhance class="bg-amber-600 max-w-xl m-auto p-3">
		<fieldset disabled={submitting}>
			<input
				type="file"
				class="hidden"
				id="imageInput"
				accept="image/png, image/jpeg"
				onchange={(e) => (inputFile = (e.target as HTMLInputElement).files?.item(0))}
			/>

			<div
				id="dropzone"
				class="flex justify-center items-center border-dashed border-2 mt-10 min-h-64 rounded-md"
				class:w-full={inputFile}
				role="region"
				{ondragenter}
				{ondragleave}
				{ondrop}
				ondragover={(e) => e.preventDefault()}
			>
				{#if inputFile}
					<div class="relative my-2">
						<button
							class="absolute top-0 right-0 p-1 rounded-bl-md transition-colors text-red-700 hover:text-black hover:bg-red-700"
							type="button"
							onclick={() => (inputFile = null)}
						>
							<span class="material-symbols-outlined"> close </span>
						</button>
						<img
							src={URL.createObjectURL(inputFile)}
							alt="Previsualización"
							class="max-h-80 m-auto"
						/>
					</div>
				{:else}
					<p>
						Arrastre o <label
							for="imageInput"
							class="text-blue-100 hover:pb-0.5 hover:cursor-pointer border-b-2 transition-all"
							>seleccione un archivo</label
						>.
					</p>
				{/if}
			</div>

			<Errors errors={fileErrors} />
			<TextInput
				name="altText"
				label="Texto Alternativo"
				type="text"
				bind:value={$form.altText}
				errors={$errors.altText}
				{...$constraints}
			/>
			<button class="bg-green-200 hover:bg-amber-200 p-2 rounded-md">Crear</button>
		</fieldset>
	</form>
</div>

<style>
	:global(#dropzone.hovering) {
		background-color: rgba(0, 0, 0, 0.5);
	}
</style>
