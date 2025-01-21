<script lang="ts">
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import { MdtoHTML } from '$lib/utilities/markdown';
	import { PUBLIC_imageURL } from '$env/static/public';
	import * as enums from '$lib/utilities/enums';
	import Movable from '$lib/components/input/Movable.svelte';
	import Borders from '$lib/components/input/Borders.svelte';
	import '$lib/styles/markdown.css';
	import MainPageImage from '$lib/components/input/MainPageImage.svelte';

	const { data }: { data: PageData } = $props();
	let originalMainPages = $state($state.snapshot(data.mainPageImages));
	let updatedMainPageImages = $state($state.snapshot(data.mainPageImages));
	let preview: boolean = $state(false);
</script>

{#snippet MainImage(image: any)}
	<div
		class="flex size-full"
		style={`justify-content: ${
			image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.LEFT
				? 'start'
				: image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.RIGHT
					? 'end'
					: 'center'
		};`}
		class:flex-row={image.mainImageConfig.desktopConfig.descriptionPosition == enums.Directions.E ||
			image.mainImageConfig.desktopConfig.logoPosition == enums.Directions.E}
		class:flex-row-reverse={image.mainImageConfig.desktopConfig.descriptionPosition ==
			enums.Directions.W || image.mainImageConfig.desktopConfig.logoPosition == enums.Directions.W}
	>
		<Movable
			left={() => {
				if (
					image.mainImageConfig.desktopConfig.descriptionPosition ||
					image.mainImageConfig.desktopConfig.logoPosition
				) {
					// If there's a description or logo only change between right and left
					image.mainImageConfig.desktopConfig.imagePosition = enums.DesktopPosition.LEFT;
					if (image.mainImageConfig.desktopConfig.descriptionPosition)
						image.mainImageConfig.desktopConfig.descriptionPosition = enums.Directions.E;
					if (image.mainImageConfig.desktopConfig.logoPosition)
						image.mainImageConfig.desktopConfig.logoPosition = enums.Directions.E;
				} else {
					// Otherwise interpolate between left, center, right.
					const enumValues = Object.values(enums.DesktopPosition);
					const currentValue = image.mainImageConfig.desktopConfig.imagePosition;
					const currentIndex = enumValues.indexOf(currentValue);
					image.mainImageConfig.desktopConfig.imagePosition =
						enumValues[currentIndex - 1] || currentValue;
				}
			}}
			right={() => {
				if (
					image.mainImageConfig.desktopConfig.descriptionPosition ||
					image.mainImageConfig.desktopConfig.logoPosition
				) {
					// If there's a description or logo only change between right and left
					image.mainImageConfig.desktopConfig.imagePosition = enums.DesktopPosition.RIGHT;
					if (image.mainImageConfig.desktopConfig.descriptionPosition)
						image.mainImageConfig.desktopConfig.descriptionPosition = enums.Directions.W;
					if (image.mainImageConfig.desktopConfig.logoPosition)
						image.mainImageConfig.desktopConfig.logoPosition = enums.Directions.W;
				} else {
					const enumValues = Object.values(enums.DesktopPosition);
					const currentValue = image.mainImageConfig.desktopConfig.imagePosition;
					const currentIndex = enumValues.indexOf(currentValue);
					image.mainImageConfig.desktopConfig.imagePosition =
						enumValues[currentIndex + 1] || currentValue;
				}
			}}
			bind:preview
			class="relative h-full w-fit flex-shrink-0"
		>
			<img
				src={`${PUBLIC_imageURL}${image.filename}`}
				alt={image.altText}
				class="h-full transition-all"
				class:p-8={image.mainImageConfig.desktopConfig.overflow}
			/>
			<div class="absolute top-0 w-full flex justify-between" class:hidden={preview}>
				<div class="flex rounded-br-sm">
					<button
						class="text-white hover:bg-gray-200/40 p-2 transition-colors size-10"
						title={image.mainImageConfig.desktopConfig.descriptionPosition
							? 'Remover descripción'
							: 'Añadir descripción'}
						onclick={() => {
							if (!image.mainImageConfig.desktopConfig.descriptionPosition) {
								const newPosition =
									image.mainImageConfig.desktopConfig.logoPosition || enums.Directions.E;
								image.mainImageConfig.desktopConfig.descriptionPosition = newPosition;
								image.mainImageConfig.desktopConfig.imagePosition =
									newPosition == enums.Directions.E
										? enums.DesktopPosition.LEFT
										: enums.DesktopPosition.RIGHT;
							} else image.mainImageConfig.desktopConfig.descriptionPosition = null;
						}}
					>
						<span class="material-symbols-outlined">
							{image.mainImageConfig.desktopConfig.descriptionPosition ? 'delete' : 'description'}
						</span>
					</button>
					<button
						title="Logo"
						class="size-10 p-2 hover:bg-gray-200/40"
						onclick={() => {
							if (!image.mainImageConfig.desktopConfig.logoPosition) {
								const newPosition =
									image.mainImageConfig.desktopConfig.descriptionPosition || enums.Directions.E;
								image.mainImageConfig.desktopConfig.logoPosition = newPosition;
								image.mainImageConfig.desktopConfig.descriptionLogoPosition = enums.Directions.N;
								image.mainImageConfig.desktopConfig.imagePosition =
									newPosition == enums.Directions.E
										? enums.DesktopPosition.LEFT
										: enums.DesktopPosition.RIGHT;
							} else {
								image.mainImageConfig.desktopConfig.logoPosition = null;
							}
						}}
					>
						<img src={symbol} alt="symbol" class="size-full" />
					</button>
				</div>
				<button
					class="absolute top-0 right-0 text-white hover:bg-gray-200/40 rounded-bl-sm transition-colors size-10 p-2"
					title="Sangrar"
					onclick={() => {
						image.mainImageConfig.desktopConfig.overflow =
							!image.mainImageConfig.desktopConfig.overflow;
					}}
				>
					<span class="material-symbols-outlined">
						{image.mainImageConfig.desktopConfig.overflow
							? 'photo_size_select_large'
							: 'photo_size_select_small'}
					</span>
				</button>
			</div>
		</Movable>
		{#if image.mainImageConfig.desktopConfig.descriptionPosition || image.mainImageConfig.desktopConfig.logoPosition}
			<div
				class="size-full flex flex-col items-center justify-around"
				class:flex-col-reverse={image.mainImageConfig.desktopConfig.descriptionLogoPosition ===
					enums.Directions.S}
			>
				{#if image.mainImageConfig.desktopConfig.logoPosition}
					{#if !preview}
						<Movable
							up={image.mainImageConfig.desktopConfig.descriptionLogoPosition !==
								enums.Directions.N && image.mainImageConfig.desktopConfig.descriptionPosition
								? () => {
										image.mainImageConfig.desktopConfig.descriptionLogoPosition =
											enums.Directions.N;
									}
								: undefined}
							down={image.mainImageConfig.desktopConfig.descriptionLogoPosition !==
								enums.Directions.S && image.mainImageConfig.desktopConfig.descriptionPosition
								? () => {
										image.mainImageConfig.desktopConfig.descriptionLogoPosition =
											enums.Directions.S;
									}
								: undefined}
							bind:preview
							class="h-1/2 w-fit"
						>
							<Borders
								class="h-full w-fit relative"
								id={`logo-${image.id}`}
								bind:n={image.mainImageConfig.desktopConfig.logoBorders.n}
								bind:s={image.mainImageConfig.desktopConfig.logoBorders.s}
								bind:e={image.mainImageConfig.desktopConfig.logoBorders.e}
								bind:w={image.mainImageConfig.desktopConfig.logoBorders.w}
							>
								<img src={symbol} alt="symbol" class="h-full w-fit" />
							</Borders>
						</Movable>
					{:else}
						<div class="h-1/2 w-fit">
							<img
								src={symbol}
								alt="symbol"
								class="h-full w-fit border-vector-orange p-5"
								class:border-t-4={image.mainImageConfig.desktopConfig.logoBorders.n}
								class:border-b-4={image.mainImageConfig.desktopConfig.logoBorders.s}
								class:border-r-4={image.mainImageConfig.desktopConfig.logoBorders.e}
								class:border-l-4={image.mainImageConfig.desktopConfig.logoBorders.w}
							/>
						</div>
					{/if}
				{/if}
				{#if image.mainImageConfig.desktopConfig.descriptionPosition}
					{#if !preview}
						<div class="flex items-center justify-center w-full">
							<Borders
								id={`description-${image.id}`}
								bind:n={image.mainImageConfig.desktopConfig.descriptionBorders.n}
								bind:s={image.mainImageConfig.desktopConfig.descriptionBorders.s}
								bind:e={image.mainImageConfig.desktopConfig.descriptionBorders.e}
								bind:w={image.mainImageConfig.desktopConfig.descriptionBorders.w}
								class="w-full mx-20"
							>
								<div class="flex justify-between my-5">
									<div class="flex flex-col">
										<label for={`main-image-desc-alignment-${image.id}`} class="text-white"
											>Alineación</label
										>
										<select
											id={`main-image-desc-alignment-${image.id}`}
											bind:value={image.mainImageConfig.descriptionAlignment}
										>
											{#each Object.entries(enums.TextAlignment) as [key, val] (key)}
												<option value={val}>{key}</option>
											{/each}
										</select>
									</div>
									<div class="flex flex-col">
										<label for={`main-image-desc-font-${image.id}`} class="text-white"
											>Tipografía</label
										>
										<select
											id={`main-image-desc-font-${image.id}`}
											bind:value={image.mainImageConfig.descriptionFont}
										>
											{#each Object.entries(enums.TextFont) as [key, val] (key)}
												<option value={val}>{key}</option>
											{/each}
										</select>
									</div>
								</div>
								<textarea
									class={`text-white bg-transparent border-2 border-dashed w-full border-white h-20 ${image.mainImageConfig.descriptionAlignment} font-${image.mainImageConfig.descriptionFont}`}
									bind:value={image.mainImageConfig.descriptionEs}
								></textarea>
							</Borders>
						</div>
					{:else}
						<div
							class={`markdownDescription text-white w-2/3 p-2 border-vector-orange ${image.mainImageConfig.descriptionAlignment} font-${image.mainImageConfig.descriptionFont}`}
							class:border-t-4={image.mainImageConfig.desktopConfig.descriptionBorders.n}
							class:border-b-4={image.mainImageConfig.desktopConfig.descriptionBorders.s}
							class:border-r-4={image.mainImageConfig.desktopConfig.descriptionBorders.e}
							class:border-l-4={image.mainImageConfig.desktopConfig.descriptionBorders.w}
						>
							{@html MdtoHTML(image.mainImageConfig.descriptionEs)}
						</div>
					{/if}
				{/if}
			</div>
		{/if}
	</div>
{/snippet}

<div
	class="bg-black relative hidden md:block"
	class:h-screen={preview}
	class:overflow-y-scroll={preview}
	class:snap-y={preview}
	class:snap-mandatory={preview}
>
	<input id="previewToggle" type="checkbox" bind:checked={preview} hidden />
	<label
		for="previewToggle"
		title="Vista Previa"
		class="fixed top-5 right-5 hover:cursor-pointer z-10 bg-gray-200/30 hover:bg-gray-200 rounded-sm"
	>
		<span class="material-symbols-outlined text-4xl">
			{preview ? 'preview_off' : 'preview'}
		</span>
	</label>
	<div class="h-screen snap-center min-h-96">
		<header class="bg-vector-grey p-5 h-24">
			<img src={logo} alt="Vector Interior Design" class="m-auto h-full" id="logo" />
		</header>
		{#each updatedMainPageImages.slice(0, 1) as image, i (image.filename)}
			<Movable
				down={() => {
					const fromIndex = i;
					const element = updatedMainPageImages.splice(fromIndex, 1)[0];
					updatedMainPageImages.splice(fromIndex + 1, 0, element);
				}}
				style="height: calc(100vh - 6rem);"
				class="min-h-[18rem]"
				bind:preview
			>
				{@render MainImage(image)}
			</Movable>
		{/each}
	</div>
	{#each updatedMainPageImages.slice(1) as image, i (image.filename)}
		<Movable
			up={() => {
				const fromIndex = i + 1; // Adding once since the first image is at the top then it should start at index 1
				const element = updatedMainPageImages.splice(fromIndex, 1)[0];
				updatedMainPageImages.splice(fromIndex - 1, 0, element);
			}}
			down={i + 1 !== updatedMainPageImages.length - 1
				? () => {
						const fromIndex = i + 1;
						const element = updatedMainPageImages.splice(fromIndex, 1)[0];
						updatedMainPageImages.splice(fromIndex + 1, 0, element);
					}
				: undefined}
			bind:preview
		>
			<div
				class="h-screen min-h-96 snap-center bg-black"
				class:border-dashed={!preview}
				class:border-t-2={!preview}
			>
				{@render MainImage(image)}
			</div>
		</Movable>
	{/each}
</div>

<div class="flex p-10 items-center md:hidden bg-black h-screen">
	<h1 class="text-4xl text-white h-fit text-center border-dashed border-2 border-white p-10">
		Pantalla muy pequeña para mostrar este contenido. Intente rotar el dispositivo.
	</h1>
</div>
