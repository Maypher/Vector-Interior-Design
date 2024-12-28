<script lang="ts">
	import { PUBLIC_imageURL } from '$env/static/public';
	import { Directions } from '$lib/utilities/enums';
	import Markdown from '../markdown/Markdown.svelte';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';

	interface ImageConfig {
		id: number;
		description: string | undefined;
		descriptionEn: string | undefined;
		descriptionPos: string | null;
		logoPos: string | null;
		overflow: boolean;
	}

	interface Props {
		image: {
			filename: string;
			altText: string;
			ambienteId: number;
			obraId: number;
		};
		imageConfig: ImageConfig;
	}

	const { image, imageConfig }: Props = $props();

	// Done this way because prop passed by reference and when updating it updates the value in the parent.
	// This forces a deep copy so it is treated as a different value.
	let configClone = $state.snapshot(imageConfig);
	let originalConfig: ImageConfig = $state(configClone);
	let updatedConfig: ImageConfig = $state(configClone);
	let shouldUpdate: boolean = $derived(
		Object.entries(updatedConfig).some(
			([key, val]) => originalConfig[key as keyof ImageConfig] !== val
		)
	);

	let showDescriptions: boolean = $state(false);
	let descriptionEn: boolean = $state(false);

	async function onsubmit(evt: SubmitEvent) {
		evt.preventDefault();

		const query = `
			mutation updateImageConfig($id: Int!, $description: String, $descriptionEn: String, 
			$logoPos: Direction, $descriptionPos: Direction, $overflow: Boolean) {
				updateImageConfig(id: $id, description: $description, descriptionEn: $descriptionEn,
				logoPos: $logoPos, descriptionPos: $descriptionPos, overflow: $overflow) {
					description
					descriptionEn
					logoPos
					descriptionPos
					overflow
				}
			}
		`;

		const updates = $state.snapshot(updatedConfig);

		const updatedData = (await graphql(query, updates)).updateImageConfig;

		originalConfig = updatedData;
		updatedConfig = updatedData;

		success('Información actualizada correctamente.');
	}
</script>

<div class="flex justify-between pl-2 w-full">
	<a href={`/obras/${image.obraId}/ambientes/${image.ambienteId}/imagenes/${image.filename}`}>
		<img src={`${PUBLIC_imageURL}${image.filename}`} alt={image.altText} class="h-36" />
	</a>
	<form {onsubmit} class="flex">
		<div>
			<div class="flex gap-5 p-5 items-center">
				<div>
					<label for="overflow">Sangrar</label>
					<input type="checkbox" name="overflow" bind:checked={updatedConfig.overflow} />
				</div>
				<div class="flex flex-col items-center gap-2">
					<label for="logoPos">Posición del Logo</label>
					<select name="logoPos" bind:value={updatedConfig.logoPos}>
						{#each Object.entries(Directions) as [direction, value] (direction)}
							<option {value} selected={value === imageConfig.logoPos}>{direction}</option>
						{/each}
					</select>
				</div>
				<div class="flex flex-col items-center gap-2">
					<label for="textPos">Posición de Descripción</label>
					<select name="textPos" bind:value={updatedConfig.descriptionPos}>
						{#each Object.entries(Directions) as [direction, value] (direction)}
							<option {value} selected={value === imageConfig.descriptionPos}>{direction} </option>
						{/each}
					</select>
				</div>
			</div>
			<div>
				<div class="w-full bg-green-300 flex items-center p-2">
					<label for={`showDescription-${imageConfig.id}`} class="w-full select-none"
						>Descripciones</label
					>
					<input
						type="checkbox"
						id={`showDescription-${imageConfig.id}`}
						form={null}
						bind:checked={showDescriptions}
						class="hidden"
					/>
					<span
						class="material-symbols-outlined transition-transform"
						class:rotate-180={showDescriptions}
					>
						keyboard_arrow_up
					</span>
				</div>
				<div
					class="transition-all overflow-hidden"
					class:max-h-0={!showDescriptions}
					class:max-h-screen={showDescriptions}
				>
					<div class="flex w-full">
						<button
							type="button"
							class="bg-red-200 w-full hover:bg-red-500"
							class:bg-red-500={!descriptionEn}
							onclick={() => (descriptionEn = false)}>Español</button
						>
						<button
							type="button"
							class="bg-red-200 w-full hover:bg-red-500"
							class:bg-red-500={descriptionEn}
							onclick={() => (descriptionEn = true)}>Ingles</button
						>
					</div>
					<div class:hidden={!descriptionEn}>
						<Markdown
							label="Descripción (Ingles)"
							name="descriptionEn"
							bind:value={updatedConfig.descriptionEn}
							errors={[]}
						/>
					</div>
					<div class:hidden={descriptionEn}>
						<Markdown
							label="Descripción"
							name="description"
							bind:value={updatedConfig.description}
							errors={[]}
						/>
					</div>
				</div>
			</div>
		</div>
		<div
			class="flex flex-col justify-center gap-2 overflow-hidden transition-all ease-out duration-500"
			class:max-w-0={!shouldUpdate}
			class:p-2={shouldUpdate}
		>
			<button
				type="submit"
				class="text-green-600 hover:bg-green-600 hover:text-white rounded-md transition-all"
				title="Guardar cambios"
				><span class="material-symbols-outlined h-full content-center"> check </span></button
			>
			<button
				type="button"
				class="text-red-600 hover:bg-red-600 hover:text-white rounded-md transition-all"
				title="Revertir cambios"
				onclick={() => (updatedConfig = configClone)}
				><span class="material-symbols-outlined h-full content-center"> cancel </span></button
			>
		</div>
	</form>
</div>
