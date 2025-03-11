<script lang="ts">
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import logoWhite from '$lib/images/logo white.svg';
	import type { PageData } from './$types';
	import tony from '$lib/images/tony.jpg';
	import tonyContact from '$lib/images/contact.jpg';
	import { Directions, DesktopPosition } from '$lib/utilities/enums';
	import { onMount } from 'svelte';
	import mdToHtml from '$lib/utilities/markdown';
	import '$lib/styles/markdown.css';
	import { getI18n } from '$lib/i18n';

	interface Borders {
		n: boolean;
		s: boolean;
		e: boolean;
		w: Boolean;
	}

	interface mainImageData {
		filename: string;
		imageUrl: string;
		altText: string;
		mainImageConfig: {
			description?: string;
			descriptionFontSize: string;
			descriptionFont: string;
			descriptionAlignment: string;
			phoneConfig: {
				overflow?: boolean;
				imageBorders: Borders;
				logoBorders: Borders;
				descriptionPosition?: 'N' | 'S' | 'E' | 'W';
				logoPosition?: 'N' | 'S' | 'E' | 'W';
			};
			desktopConfig: {
				overflow: boolean;
				imagePosition: 'N' | 'S' | 'E' | 'W';
				descriptionPosition: 'N' | 'S' | 'E' | 'W';
				descriptionBorders: Borders;
				logoPosition: 'N' | 'S' | 'E' | 'W';
				descriptionLogoPosition: 'N' | 'S' | 'E' | 'W';
				logoBorders: Borders;
			};
		};
	}

	const { data }: { data: PageData } = $props();
	const mainImages: mainImageData[] = data.mainImages;

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

		const pencil = document.getElementById('nav');
		if (pencil) pencilObserver.observe(pencil);
	});

	const i18n = getI18n();
</script>

{#snippet mainImage(imageData: mainImageData)}
	<div
		class="flex size-full gap-20 lg:hidden"
		class:flex-col={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.N}
		class:flex-col-reverse={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.S}
	>
		{#if imageData.mainImageConfig.phoneConfig.logoPosition}
			<div
				class={`border-vector-orange m-auto w-10/12 ${imageData.mainImageConfig.phoneConfig.logoBorders.n ? 'border-t-2 pt-10' : ''} ${imageData.mainImageConfig.phoneConfig.logoBorders.s ? 'border-b-2 pb-10' : ''} ${imageData.mainImageConfig.phoneConfig.logoBorders.e ? 'border-r-2 pr-10' : ''} ${imageData.mainImageConfig.phoneConfig.logoBorders.w ? 'border-l-2 pl-10' : ''}`}
			>
				<img src={symbol} alt="V" class="mx-auto w-20" />
			</div>
		{/if}
		<figure
			class={`flex size-full items-center ${
				imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.S
					? 'flex-col-reverse'
					: ''
			} ${imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.N ? 'flex-col' : 'flex-col-reverse'}`}
		>
			{#if imageData.mainImageConfig.phoneConfig.descriptionPosition && imageData.mainImageConfig.description}
				<figcaption class="flex w-10/12 grow flex-col justify-center text-white">
					<div
						class={`text-white ${imageData.mainImageConfig.descriptionAlignment} markdownDescription my-16`}
						style={`font-family: ${imageData.mainImageConfig.descriptionFont};`}
					>
						{@html mdToHtml(imageData.mainImageConfig.description)}
					</div>
				</figcaption>
			{/if}
			<div
				class={`border-vector-orange mx-auto ${!imageData.mainImageConfig.phoneConfig.overflow ? 'w-5/6' : ''} ${imageData.mainImageConfig.phoneConfig.imageBorders.e ? 'border-r-2 pr-20' : ''}`}
			>
				{#if imageData.mainImageConfig.phoneConfig.imageBorders.n}
					<div class="bg-vector-orange max-w-83/10 mx-auto mb-20 h-px w-full"></div>
				{/if}
				<img src={imageData.imageUrl} alt={imageData.altText} />
				{#if imageData.mainImageConfig.phoneConfig.imageBorders.s}
					<div class="bg-vector-orange max-w-83/10 mx-auto mt-20 h-px w-full"></div>
				{/if}
			</div>
		</figure>
	</div>

	<figure
		class={`m-auto hidden size-full items-center lg:flex ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.LEFT &&
			!imageData.mainImageConfig.desktopConfig.overflow
				? 'xl:pl-20'
				: ''
		} ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.RIGHT &&
			!imageData.mainImageConfig.desktopConfig.overflow
				? 'xl:pr-20'
				: ''
		} ${
			imageData.mainImageConfig.desktopConfig.descriptionPosition == Directions.E ||
			imageData.mainImageConfig.desktopConfig.logoPosition == Directions.E
				? 'flex-row'
				: ''
		} ${
			imageData.mainImageConfig.desktopConfig.descriptionPosition == Directions.W ||
			imageData.mainImageConfig.desktopConfig.logoPosition == Directions.W
				? 'flex-row-reverse'
				: ''
		}`}
		style={`justify-content: ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.LEFT
				? 'start'
				: imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.RIGHT
					? 'end'
					: 'center'
		};`}
	>
		<img
			src={imageData.imageUrl}
			alt={imageData.altText}
			class="h-full max-w-full transition-all"
		/>

		{#if imageData.mainImageConfig.desktopConfig.descriptionPosition || imageData.mainImageConfig.desktopConfig.logoPosition}
			<figcaption
				class={`max-w-1/2 m-auto flex h-full flex-col items-center justify-around ${
					imageData.mainImageConfig.desktopConfig.descriptionLogoPosition === Directions.S
						? 'flex-col-reverse'
						: ''
				}`}
			>
				{#if imageData.mainImageConfig.desktopConfig.logoPosition}
					<div class="h-1/2 w-fit">
						<img
							src={symbol}
							alt="V"
							class="border-vector-orange h-full w-fit p-5"
							class:border-t-4={imageData.mainImageConfig.desktopConfig.logoBorders.n}
							class:border-b-4={imageData.mainImageConfig.desktopConfig.logoBorders.s}
							class:border-r-4={imageData.mainImageConfig.desktopConfig.logoBorders.e}
							class:border-l-4={imageData.mainImageConfig.desktopConfig.logoBorders.w}
						/>
					</div>
				{/if}
				{#if imageData.mainImageConfig.desktopConfig.descriptionPosition && imageData.mainImageConfig.description}
					<div
						class={`markdownDescription border-vector-orange text-white ${imageData.mainImageConfig.descriptionAlignment} font-${imageData.mainImageConfig.descriptionFont}`}
						class:border-t-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.n}
						class:border-b-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.s}
						class:border-r-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.e}
						class:border-l-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.w}
					>
						{@html mdToHtml(imageData.mainImageConfig.description)}
					</div>
				{/if}
			</figcaption>
		{/if}
	</figure>
{/snippet}

<header class="bg-vector-grey flex h-28 items-center justify-center gap-20 p-5">
	<a href={`/${$i18n.language}`} class="hover:scale-120 h-full transition-transform">
		<img src={logo} alt="Vector: Interior Design" class="h-full" />
	</a>
</header>

{#each mainImages.slice(0, 1) as image (image.filename)}
	<div
		class={`mb-50 h-[calc(100svh-7rem)] ${image.mainImageConfig.desktopConfig.overflow ? 'lg:h-[calc(100svh-7rem)]' : 'lg:mt-20 lg:h-[calc(80svh-7rem)]'}`}
	>
		{@render mainImage(image)}
	</div>
{/each}

{#each mainImages.slice(1, 5) as image (image.filename)}
	<div
		class={`my-50 ${image.mainImageConfig.desktopConfig.overflow ? 'lg:h-[100vh]' : 'lg:h-[80vh]'}`}
	>
		{@render mainImage(image)}
	</div>
{/each}

<figure
	class="lg:my-50 my-50 relative flex flex-col items-center justify-start gap-x-5 gap-y-10 lg:ml-10 lg:h-[85vh] lg:flex-row xl:ml-20"
>
	<img src={tony} alt="Diseñador" class="max-h-[60vh] lg:max-h-[70vh]" />
	<figcaption
		class="mx-auto flex h-full w-3/4 flex-col items-center justify-center gap-20 text-justify indent-3 text-lg text-white lg:w-1/2 lg:items-end"
	>
		<p>
			{$i18n.t('mainPageMsg')}
		</p>
		<img src={logoWhite} alt="Vector: Interior Design" class="w-44" />
	</figcaption>
</figure>

{#each mainImages.slice(5, 8) as image (image.filename)}
	<div
		class={`lg:my-50 my-50 ${image.mainImageConfig.desktopConfig.overflow ? 'lg:h-[100vh]' : 'lg:h-[80vh]'}`}
	>
		{@render mainImage(image)}
	</div>
{/each}

<div
	class="border-vector-orange lg:my-50 my-50 m-auto w-5/6 border-2 py-8 text-center font-[Bahnschrift] text-2xl font-thin tracking-[0.5rem] text-white md:w-fit md:px-6 md:text-4xl"
	style="word-spacing: 1rem;"
>
	Interior Design
</div>

{#each mainImages.slice(8, -1) as image (image.filename)}
	<div
		class={`lg:my-50 my-50 ${image.mainImageConfig.desktopConfig.overflow ? 'lg:h-[100vh]' : 'lg:h-[80vh]'}`}
	>
		{@render mainImage(image)}
	</div>
{/each}

<div
	class="lg:my-50 lg:ml-15 mt-20 flex h-screen flex-col gap-y-10 overflow-hidden p-10 lg:h-[70vh] lg:flex-row lg:justify-between xl:h-[90vh] xl:justify-evenly"
	id="nav"
>
	<img
		src={mainImages.at(-1)!.imageUrl}
		alt={mainImages.at(-1)!.altText}
		class="lg:max-w-2/3 max-w-full lg:my-auto lg:max-h-full"
	/>
	<ul class="relative flex size-full items-center justify-center gap-5 p-5">
		<li
			class="hover-link relative top-10 h-fit w-fit text-4xl text-white md:max-lg:top-20"
			style="font-family: Agency-FB;"
		>
			<a href={`${$i18n.language}/esculturas/`}>
				{$i18n.t('sculptures')}
			</a>
		</li>
		<div class="-z-10 flex size-full w-[2px] flex-col items-center overflow-visible" id="pencil">
			<img src={symbol} alt="V" class="min-h-32 min-w-32" />
			<div class="bg-vector-orange relative bottom-5 h-full w-[2px]"></div>
		</div>
		<li
			class="hover-link relative bottom-0 w-fit text-4xl text-white after:relative after:top-1 md:max-lg:bottom-0"
			style="font-family: Agency-FB;"
		>
			<a href={`/${$i18n.language}/proyectos/`}>
				{$i18n.t('projects')}
			</a>
		</li>
	</ul>
</div>

<footer class="my-15 relative flex flex-col items-center justify-center gap-10 lg:flex-row">
	<div class="max-w-4/5 lg:max-w-6/7 relative grid gap-y-5">
		<div
			class="md:leading-16 leading-12 flex size-fit flex-col self-end justify-self-start text-[3rem] text-white md:gap-4 md:text-[5rem]"
			style="font-family: Agency-FB;"
		>
			<p>CON</p>
			<p class="indent-[2.1ch]">TAC{$i18n.language === 'en' ? 'T' : ''}</p>
			{#if $i18n.language === 'es'}
				<p
					class="col-start-2 row-start-2 text-center indent-[3.9ch] text-white"
					style="font-family: Agency-FB;"
				>
					TO
				</p>
			{/if}
		</div>
		<img
			src={tonyContact}
			alt="Contacto"
			class="col-start-2 block max-h-[70vh] align-middle xl:max-h-[80vh]"
		/>
		<a
			href="mailto:k@vectorinterior.design"
			class="font-Agency-FB col-start-2 row-start-2 justify-self-center text-2xl text-white"
		>
			contact@vectorinterior.design
		</a>
	</div>
	<img
		src={logoWhite}
		alt="Vector: Interior Design"
		class="bottom-0 right-20 w-1/2 max-w-32 lg:absolute"
	/>
</footer>

<style>
	.hover-link::after {
		display: block;
		content: '';
		background-color: var(--color-vector-orange);
		height: 0.13rem;
		width: 100%;
		transition: all 0.3s ease-out;
		transform: scale(0, 1);
	}

	.hover-link:hover::after {
		transform: scale(1, 1);
	}

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
