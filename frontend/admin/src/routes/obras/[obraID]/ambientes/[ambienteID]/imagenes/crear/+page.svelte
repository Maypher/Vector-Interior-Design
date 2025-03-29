<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import { yup } from 'sveltekit-superforms/adapters';
	import { createImageSchema } from '$lib/utilities/yupSchemas';
	import { error } from '$lib/utilities/toasts';
	import { goto } from '$app/navigation';
	import Errors from '$lib/components/input/Errors.svelte';
	import { PUBLIC_apiURL } from '$env/static/public';

	const { data }: { data: PageData } = $props();
	let inputFile: File | undefined | null = $state();
	let fileErrors: Array<string> = $state([]);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.createForm, {
		SPA: true,
		validators: yup(createImageSchema),
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
                        $altTextEs: String!,
						$altTextEn: String!,
                        ) {
                        createImage(
                            spaceId: $spaceId,
                            image: $file,
                            altTextEs: $altTextEs,
							altTextEn: $altTextEn
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
					altTextEs: createForm.data.altTextEs,
					altTextEn: createForm.data.altTextEn,
					spaceId: data.ambienteID
				};

				const operations = JSON.stringify({ query, variables });
				const map = JSON.stringify({ file: ['variables.file'] });

				let formData = new FormData();

				formData.append('operations', operations);
				formData.append('map', map);
				formData.append('file', inputFile);

				const res = await fetch(`https://${PUBLIC_apiURL}/graphql/`, {
					method: 'POST',
					body: formData,
					credentials: 'include'
				});

				if (res.ok) {
					const imageData = (await res.json()).data.createImage;

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
							await goto(`/obras/${data.projectId}`);
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

<div class="bg-black flex items-center justify-center p-5 min-h-[calc(100svh-5rem)]">
	<form use:enhance class="bg-gray-700 max-w-xl w-full p-3 rounded-md">
		<fieldset disabled={submitting} class="flex flex-col gap-5">
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
							>seleccione un archivo
						</label>.
					</p>
				{/if}
			</div>

			<Errors errors={fileErrors} />
			<div class="flex flex-col gap-2">
				<label for="alt-text-es" class="text-white">Texto alternativo</label>
				<input
					type="text"
					id="alt-text-es"
					class="bg-white rounded-md p-2"
					maxlength="255"
					bind:value={$form.altTextEs}
				/>
			</div>
			<div class="flex flex-col gap-2">
				<label for="alt-text-en" class="text-white">Texto alternativo (Ingles)</label>
				<input
					type="text"
					id="alt-text-en"
					class="bg-white rounded-md p-2"
					bind:value={$form.altTextEn}
					maxlength="255"
				/>
			</div>
			<button
				type="submit"
				class="bg-green-200 hover:cursor-pointer hover:bg-amber-200 p-2 rounded-md self-start"
				>Crear
			</button>
		</fieldset>
	</form>
</div>

<style>
	:global(#dropzone.hovering) {
		background-color: rgba(0, 0, 0, 0.5);
	}
</style>
