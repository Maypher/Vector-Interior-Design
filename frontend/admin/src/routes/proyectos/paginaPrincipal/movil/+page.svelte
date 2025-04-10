<script lang="ts">
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import logoWhite from '$lib/images/logo white.svg';
	import tony from '$lib/images/tony.jpg';
	import { Directions, TextAlignment, TextFont } from '$lib/utilities/enums';
	import '$lib/styles/markdown.css';
	import Movable from '$lib/components/editor/Movable.svelte';
	import Borders from '$lib/components/editor/Borders.svelte';
	import { isEqual, cloneDeep } from 'lodash-es';
	import { onMount } from 'svelte';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import { success } from '$lib/utilities/toasts';
	import graphql from '$lib/utilities/api';
	import Phone from '$lib/components/layout/phone.svelte';
	import EditorDescription from '$lib/components/editor/EditorDescription.svelte';
	import BgColor from '$lib/components/editor/BgColor.svelte';
	import { mdToHTML } from '$lib/utilities/markdown';

	const { data }: { data: PageData } = $props();
	let originalMainPages: any[] = $state($state.snapshot(data.mainPageImages));
	let updatedMainPageImages: any[] = $state($state.snapshot(data.mainPageImages));

	let preview: boolean = $state(false);
	let saveEnabled: boolean = $derived(!isEqual(originalMainPages, updatedMainPageImages));
	let englishDescription: boolean = $state(false);

	async function updatedMainPagePhone() {
		const query = `
			mutation updateMainPageImage($id: Int!, $descriptionEs: String, $descriptionEn: String, 
				$descriptionAlignment: String, $descriptionFont: String, $index: Int, $bgColor: String
				$phoneConfig: MainPageImagePhoneConfigInput) {
				updateMainPageConfig(id: $id, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, 
				descriptionAlignment: $descriptionAlignment, descriptionFont: $descriptionFont, index: $index, 
				phoneConfig: $phoneConfig, bgColor: $bgColor) {
					id
					descriptionEs
					descriptionEn
					descriptionFont
					descriptionAlignment
					bgColor
					phoneConfig {
						descriptionPosition
						logoPosition
						imageBorders {
							n
							s
							e
							w
						}
						logoBorders {
							n
							s
							e
							w
						}
						overflow
					}
					image {
						id
						filename
						altTextEs
						imageUrl
					}
				}
			}
		`;

		const originalOrder = originalMainPages.map((x) => x.mainImageConfig.id);
		const updatedOrder = updatedMainPageImages.map((x) => x.mainImageConfig.id);
		const ordersToUpdate = getArrayDifference(originalOrder, updatedOrder);
		let updatedValues: any[] = [];

		for (const [i, image] of updatedMainPageImages.entries()) {
			// If there aren't any changes between the original and updated config then don't updated it in the backend.
			if (!isEqual(image, originalMainPages.at(i))) {
				const mainPageConfig = image.mainImageConfig;
				const variables = {
					id: mainPageConfig.id,
					descriptionEs: mainPageConfig.descriptionEs,
					descriptionEn: mainPageConfig.descriptionEn,
					descriptionAlignment: mainPageConfig.descriptionAlignment,
					index: ordersToUpdate.find((val) => val.id === mainPageConfig.id)?.newPos,
					phoneConfig: mainPageConfig.phoneConfig,
					bgColor: mainPageConfig.bgColor
				};

				const { image: updatedImage, ...updatedData } = (await graphql(query, variables))
					.updateMainPageConfig;

				const resObject = {
					...updatedImage,
					mainImageConfig: {
						...updatedData
					}
				};

				updatedValues.push(resObject);
			} else updatedValues.push(image); // Just add it to the new list to keep the order
		}

		originalMainPages = updatedValues;
		// Doing this way because if it assigns it directly  then both originalMainPage and updatedMainPageImages
		// reference the same object and updates affect both variables.
		updatedMainPageImages = cloneDeep(updatedValues);
		success('Página principal actualizada con éxito.');
	}

	onMount(() => {
		const pencilObserver = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						const pencil = document.getElementById('pencil');
						if (pencil) {
							pencil.id = '';
							pencil.classList.add('pencil-animate');
							pencilObserver.unobserve(entry.target);
						}
					}
				});
			},
			{
				threshold: 0.6
			}
		);

		const pencil = document.getElementById('pencil-wrapper');
		if (pencil) pencilObserver.observe(pencil);
	});

	function scrollToTop() {
		window.scrollTo({ top: 0, behavior: 'smooth' });
	}
</script>

{#snippet mainImage(imageData: any)}
	<div
		class="@md:hidden h-full"
		class:flex-col={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.N}
		class:flex-col-reverse={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.S}
	>
		{#if imageData.mainImageConfig.phoneConfig.logoPosition}
			<Movable
				up={imageData.mainImageConfig.phoneConfig.logoPosition !== Directions.N
					? () => (imageData.mainImageConfig.phoneConfig.logoPosition = Directions.N)
					: undefined}
				down={imageData.mainImageConfig.phoneConfig.logoPosition !== Directions.S
					? () => (imageData.mainImageConfig.phoneConfig.logoPosition = Directions.S)
					: undefined}
				class="border-white px-8 h-fit!"
				bind:preview
			>
				<Borders
					id={`logo-${imageData.filename}`}
					bind:n={imageData.mainImageConfig.phoneConfig.logoBorders.n}
					bind:s={imageData.mainImageConfig.phoneConfig.logoBorders.s}
					bind:e={imageData.mainImageConfig.phoneConfig.logoBorders.e}
					bind:w={imageData.mainImageConfig.phoneConfig.logoBorders.w}
					bind:preview
				>
					<img src={symbol} alt="symbol" class="mx-auto w-20" />
				</Borders>
			</Movable>
		{/if}
		<div
			class={`flex h-full items-center ${
				imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.S
					? 'flex-col-reverse'
					: ''
			} ${imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.N ? 'flex-col' : ''}`}
		>
			{#if imageData.mainImageConfig.phoneConfig.descriptionPosition}
				<Movable
					up={imageData.mainImageConfig.phoneConfig.descriptionPosition !== Directions.N
						? () => (imageData.mainImageConfig.phoneConfig.descriptionPosition = Directions.N)
						: undefined}
					down={imageData.mainImageConfig.phoneConfig.descriptionPosition !== Directions.S
						? () => (imageData.mainImageConfig.phoneConfig.descriptionPosition = Directions.S)
						: undefined}
					class={`grow size-auto text-vector-cream ${
						imageData.mainImageConfig.descriptionAlignment
					} markdownDescription flex flex-col justify-center max-w-5/6 ${
						imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.N
							? 'mb-16'
							: 'mt-16'
					}`}
					style={`font-family: ${imageData.mainImageConfig.descriptionFont};`}
					bind:preview
				>
					<EditorDescription
						id={imageData.id}
						bind:descriptionEs={imageData.mainImageConfig.descriptionEs}
						bind:descriptionEn={imageData.mainImageConfig.descriptionEn}
						bind:descriptionAlignment={imageData.mainImageConfig.descriptionAlignment}
						bind:descriptionFont={imageData.mainImageConfig.descriptionFont}
						bind:preview
					/>
				</Movable>
			{/if}
			{#if !preview}
				<Borders
					id={`image-${imageData.filename}`}
					bind:n={imageData.mainImageConfig.phoneConfig.imageBorders.n}
					bind:s={imageData.mainImageConfig.phoneConfig.imageBorders.s}
					bind:e={imageData.mainImageConfig.phoneConfig.imageBorders.e}
					bind:w={imageData.mainImageConfig.phoneConfig.imageBorders.w}
					class={`relative m-auto transition-all ${!imageData.mainImageConfig.phoneConfig.overflow ? 'w-5/6' : 'w-full'} h-fit`}
				>
					<img src={imageData.imageUrl} alt={imageData.altTextEs} />
					<div class="absolute top-0 flex justify-between w-full">
						<div class="bg-vector-cream/40">
							<button
								class="text-white hover:bg-gray-200/40 p-2 transition-colors size-10"
								title={imageData.mainImageConfig.phoneConfig.descriptionPosition
									? 'Remover descripción'
									: 'Añadir descripción'}
								onclick={() => {
									if (!imageData.mainImageConfig.phoneConfig.descriptionPosition) {
										imageData.mainImageConfig.phoneConfig.descriptionPosition =
											imageData.mainImageConfig.phoneConfig.logoPosition || Directions.S;
									} else imageData.mainImageConfig.phoneConfig.descriptionPosition = null;
								}}
							>
								<span class="material-symbols-outlined">
									{imageData.mainImageConfig.phoneConfig.descriptionPosition
										? 'delete'
										: 'description'}
								</span>
							</button>
							<BgColor
								imageId={imageData.filename}
								bind:color={imageData.mainImageConfig.bgColor}
							/>
							<button
								title="Logo"
								class="size-10 p-2 hover:bg-gray-200/40"
								onclick={() => {
									if (!imageData.mainImageConfig.phoneConfig.logoPosition) {
										imageData.mainImageConfig.phoneConfig.logoPosition =
											imageData.mainImageConfig.phoneConfig.descriptionPosition || Directions.S;
									} else imageData.mainImageConfig.phoneConfig.logoPosition = null;
								}}
							>
								<img src={symbol} alt="symbol" class="size-full" />
							</button>
						</div>
						<input
							type="checkbox"
							id={`overflow-${imageData.filename}`}
							hidden
							bind:checked={imageData.mainImageConfig.phoneConfig.overflow}
						/>
						<label
							for={`overflow-${imageData.filename}`}
							class="text-white hover:bg-gray-200/40 p-1 flex items-center self-start"
						>
							<span class="material-symbols-outlined">
								{imageData.mainImageConfig.phoneConfig.overflow
									? 'photo_size_select_small'
									: 'photo_size_select_large'}
							</span>
						</label>
					</div>
				</Borders>
			{:else}
				<div
					class={`relative border-vector-orange m-auto transition-all ${!imageData.mainImageConfig.phoneConfig.overflow ? 'w-5/6' : 'w-full'} ${imageData.mainImageConfig.phoneConfig.imageBorders.e ? 'border-r-2 pr-20' : ''} ${imageData.mainImageConfig.phoneConfig.imageBorders.w ? 'border-l-2 pl-20' : ''}`}
				>
					{#if imageData.mainImageConfig.phoneConfig.imageBorders.n}
						<div class="bg-vector-orange max-w-83/10 mx-auto mb-20 h-px w-full"></div>
					{/if}
					<img src={imageData.imageUrl} alt={imageData.altTextEs} />
					{#if imageData.mainImageConfig.phoneConfig.imageBorders.s}
						<div class="bg-vector-orange max-w-83/10 mx-auto mt-20 h-px w-full"></div>
					{/if}
				</div>
			{/if}
		</div>
	</div>
{/snippet}

<div class="min-h-screen bg-black flex flex-col items-center">
	<div class="fixed top-5 right-5 flex flex-col items-end gap-2 z-30 opacity-70 hover:opacity-100">
		<input id="previewToggle" type="checkbox" bind:checked={preview} hidden />
		<label
			for="previewToggle"
			title="Vista Previa"
			class="hover:cursor-pointer z-10 bg-gray-200/30 hover:bg-gray-200 rounded-xs"
		>
			<span class="material-symbols-outlined text-4xl select-none">
				{preview ? 'preview_off' : 'preview'}
			</span>
		</label>
		<button
			class="bg-green-500 disabled:brightness-50 hover:brightness-90 p-2 disabled:cursor-not-allowed rounded-xs transition-colors"
			disabled={!saveEnabled}
			onclick={updatedMainPagePhone}
		>
			Guardar
		</button>
		<button
			class="bg-red-500 disabled:brightness-50 hover:brightness-90 disabled:cursor-not-allowed p-2 rounded-xs transition-colors"
			disabled={JSON.stringify(originalMainPages) === JSON.stringify(updatedMainPageImages)}
			onclick={() => {
				updatedMainPageImages = $state.snapshot(originalMainPages);
			}}
		>
			Cancelar cambios
		</button>
	</div>

	<div class="size-full flex flex-col items-center gap-10">
		<Phone>
			<div class="flex flex-col h-full mb-20">
				<header class="flex h-22 items-center justify-between gap-20 p-5 bg-vector-cream">
					<a href="/proyectos" class="h-full">
						<img src={logo} alt="logo" class="h-full" />
					</a>
					<p>☰</p>
				</header>
				{#each updatedMainPageImages.slice(0, 1) as image, i (image.filename)}
					<div
						class="header-screen [&_.markdownDescription]:mb-0! w-full"
						style={`background-color: ${image.mainImageConfig.bgColor};`}
					>
						{@render mainImage(image)}
					</div>
				{/each}
			</div>

			{#each updatedMainPageImages.slice(1, 5) as image (image.filename)}
				<div
					class="py-20 transition-colors"
					style={`background-color: ${image.mainImageConfig.bgColor};`}
				>
					{@render mainImage(image)}
				</div>
			{/each}

			<div class="relative flex items-center pb-40 pt-20" id="about">
				<figure class="mx-auto flex flex-col items-center justify-center gap-x-20 gap-y-10 px-8">
					<img src={tony} alt="Diseñador" class="lg:h-9/10 min-h-92 h-auto w-full" />
					<figcaption>
						<p class="font-Nexa text-vector-cream whitespace-pre-line text-sm">
							<span class="text-4xl brightness-100 [&_br]:hidden [&_em]:not-italic">
								{@html mdToHTML(`Como diseñador
								de *interiores*`)}
							</span>
							<span class="mt-5 block brightness-50">
								{`mi enfoque es profundamente personal. No sigo un solo estilo, sino que fusiono influencias de distintas partes del mundo con las últimas tendencias para crear espacios únicos.

                    Mi trabajo se basa en tres pilares fundamentales: confort, funcionalidad y distinción.

                    Cada proyecto es una oportunidad para transformar ideas en ambientes que combinan estética y propósito, siempre con una atención minuciosa a los detalles. 
                    
                    Me involucro en cada etapa del proceso, porque el diseño es mi pasión y creo que la excelencia está en los detalles bien ejecutados.

                    Más que imponer un estilo, interpreto y traduzco las necesidades y aspiraciones de mis clientes en espacios que cuentan su historia. Mi trayectoria y mis proyectos hablan por si solos, respaldados por un compromiso absoluto de calidad con creatividad.`}
							</span>
						</p>
					</figcaption>
				</figure>
				<button
					class="text-vector-cream w-25 hover:scale-120 absolute bottom-10 right-1/2 cursor-pointer transition-transform translate-x-1/2"
					onclick={scrollToTop}
				>
					<img src={logoWhite} alt="Vector: Interior Design" class="w-full" />
				</button>
			</div>

			{#each updatedMainPageImages.slice(5, -1) as image (image.filename)}
				<div
					class="py-20 transition-colors"
					style={`background-color: ${image.mainImageConfig.bgColor};`}
				>
					{@render mainImage(image)}
				</div>
			{/each}

			{#each updatedMainPageImages.slice(-1) as image (image.filename)}
				<div
					class="mt-20 flex w-full flex-col gap-y-10 overflow-hidden"
					id="nav"
					style={`background-color: ${image.mainImageConfig.bgColor};`}
				>
					<img
						src={image.imageUrl}
						alt={image.altText}
						class="max-h-full max-w-full object-contain"
						style={`height: calc(${image.mainImageConfig.imageSize} / 100 * 100%);`}
					/>
					<ul class="text-vector-cream relative flex items-center justify-center gap-5 p-5 text-xl">
						<li class="hover-link font-Nexa relative top-0 z-10 h-fit w-fit">
							<a href={`/proyectos/esculturas/`} class="text-vector-cream"> Esculturas </a>
						</li>
						<div class="h-92 flex w-[2px] flex-col items-center overflow-visible" id="pencil">
							<img src={symbol} alt="V" class="min-h-20 min-w-20" />
							<div class="bg-vector-orange relative bottom-3 h-2/3 w-px"></div>
						</div>
						<li
							class="hover-link font-Nexa relative bottom-10 z-10 w-fit after:relative after:top-1"
						>
							<a href={`/proyectos/`} class="text-vector-cream"> Proyectos </a>
						</li>
					</ul>
				</div>
			{/each}

			<footer class="text-vector-cream" id="contact">
				<div class="font-Nexa relative flex items-center justify-center gap-x-5 py-20">
					<p class="border-vector-orange border-r-1 pr-5 py-2 text-2xl">Contacto</p>
					<a href="mailto:contact@vectorinterior.design" class="py-5">
						contact@vectorinterior.design
					</a>
				</div>
				<div class="bg-vector-grey flex h-24 justify-center p-6">
					<button
						onclick={scrollToTop}
						class="hover:scale-120 h-full cursor-pointer transition-transform"
					>
						<img src={logoWhite} alt="vector: Interior Design" class="h-full" />
					</button>
				</div>
			</footer>
		</Phone>
	</div>
</div>

<style>
	#pencil {
		position: relative;
		top: 110%;
	}

	.pencil-animate {
		position: relative;
		animation: pencil-draw 2s ease-in-out forwards;
	}

	@keyframes pencil-draw {
		from {
			top: 110%;
		}

		to {
			top: 0%;
		}
	}
</style>
