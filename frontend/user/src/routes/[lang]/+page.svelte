<script lang="ts">
	import Head from '$lib/components/Head.svelte';
	import { websiteUrl } from '$lib/utilities/constants';
	import symbol from '$lib/images/symbol.svg';
	import logoWhite from '$lib/images/logo white.svg';
	import type { PageData } from './$types';
	import tony from '$lib/images/tony.jpg';
	import { Directions, DesktopPosition } from '$lib/utilities/enums';
	import mdToHtml from '$lib/utilities/markdown';
	import '$lib/styles/markdown.css';
	import '$lib/styles/links.css';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import { scrollToTop } from '$lib/utilities/navigation';
	import MainPageSkeleton from '$lib/components/MainPageSkeleton.svelte';
	import NavSection from '$lib/components/NavSection.svelte';

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
			bgColor: string;
			imageSize: number;
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

	const i18n = getI18n();
</script>

<Head
	title="Vector: Interior Design"
	description={$i18n.t('googleDescription')}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en`}
	alternateEs={`${websiteUrl}/es`}
	ogTitle="Vector: Interior Design"
	ogDescription={mainImages.at(0)?.mainImageConfig.description || ''}
	imageUrl={mainImages.at(0)?.imageUrl}
/>

{#snippet mainImage(imageData: mainImageData)}
	{@const hasDescription =
		imageData.mainImageConfig.desktopConfig.descriptionPosition &&
		imageData.mainImageConfig.description}
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
				<figcaption class="max-w-5/6 flex w-fit grow flex-col justify-center text-white">
					<div
						class={`text-vector-cream ${imageData.mainImageConfig.descriptionAlignment} markdownDescription ${
							imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.N
								? 'mb-16'
								: 'mt-16'
						}`}
						style={`font-family: ${imageData.mainImageConfig.descriptionFont};`}
					>
						{@html mdToHtml(imageData.mainImageConfig.description)}
					</div>
				</figcaption>
			{/if}
			<div
				class={`border-vector-orange mx-auto ${
					!imageData.mainImageConfig.phoneConfig.overflow ? 'w-5/6' : ''
				} ${imageData.mainImageConfig.phoneConfig.imageBorders.e ? 'border-r-2 pr-20' : ''}`}
			>
				{#if imageData.mainImageConfig.phoneConfig.imageBorders.n}
					<div class="bg-vector-orange max-w-83/10 mx-auto mb-20 h-px w-full"></div>
				{/if}
				<img
					src={imageData.imageUrl}
					alt={imageData.altText}
					class="mx-auto max-h-[80vh] object-contain"
				/>
				{#if imageData.mainImageConfig.phoneConfig.imageBorders.s}
					<div class="bg-vector-orange max-w-83/10 mx-auto mt-20 h-px w-full"></div>
				{/if}
			</div>
		</figure>
	</div>

	<figure
		class={`m-auto hidden size-full max-h-full items-center gap-x-20 lg:flex ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.LEFT &&
			!imageData.mainImageConfig.desktopConfig.overflow
				? 'lg:pl-[5%]'
				: ''
		} ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.RIGHT &&
			!imageData.mainImageConfig.desktopConfig.overflow
				? 'lg:pr-[5%]'
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
			class={`${hasDescription ? 'max-w-3/5' : ''} min-h-64 object-contain`}
			style={`height: calc(${imageData.mainImageConfig.imageSize} / 100 * 100%);`}
		/>

		{#if imageData.mainImageConfig.desktopConfig.descriptionPosition || imageData.mainImageConfig.desktopConfig.logoPosition}
			<figcaption
				class="max-w-2/5 flex h-full flex-col items-center justify-around"
				class:flex-col-reverse={imageData.mainImageConfig.desktopConfig.descriptionLogoPosition ===
					Directions.S}
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
				{#if hasDescription}
					<div
						class={`markdownDescription border-vector-orange ${imageData.mainImageConfig.descriptionAlignment} font-${imageData.mainImageConfig.descriptionFont} text-vector-cream`}
						class:border-t-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.n}
						class:border-b-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.s}
						class:border-r-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.e}
						class:border-l-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.w}
					>
						{@html mdToHtml(imageData.mainImageConfig.description!)}
					</div>
				{/if}
			</figcaption>
		{/if}
	</figure>
{/snippet}

{#each mainImages.slice(0, 1) as image (image.filename)}
	<!-- Doing [&_.markdownDescription]:mb-0! because here the description should be centered in its space
 and the description by default has a margin that separates it from the Image causing it to decenter from its container-->
	<div
		class="header-screen [&_.markdownDescription]:mb-0! min-h-130 flex w-full max-lg:mb-20 xl:pr-10"
		style={`background-color: ${image.mainImageConfig.bgColor};`}
	>
		<MainPageSkeleton imageData={image} />
		<ul
			class="font-Nexa text-vector-cream relative my-auto hidden h-4/5 flex-col items-end gap-y-2 text-right text-[0.7em] max-xl:pl-10 xl:flex"
			style="letter-spacing: 0.05rem;"
		>
			<li class="before:bg-vector-orange w-fit">
				<a
					href="#about"
					class="hover-link"
					onclick={(e) => {
						e.preventDefault();

						document
							.getElementById('about')
							?.scrollIntoView({ behavior: 'smooth', block: 'center' });
					}}
				>
					{$i18n.t('about')}
				</a>
			</li>
			<li class="w-fit">
				<a href={`${$i18n.language}/proyectos`} class="hover-link">{$i18n.t('projects')}</a>
			</li>
			<li class="w-fit">
				<a href={`${$i18n.language}/esculturas`} class="hover-link">{$i18n.t('sculptures')}</a>
			</li>
			<li class="w-fit">
				<a
					href="#contact"
					class="hover-link"
					onclick={(e) => {
						e.preventDefault();

						document
							.getElementById('contact')
							?.scrollIntoView({ behavior: 'smooth', block: 'center' });
					}}
				>
					{$i18n.t('contact')}
				</a>
			</li>
		</ul>
	</div>
{/each}

{#each mainImages.slice(1, 5) as image (image.filename)}
	<div
		class="lg:min-h-120 max-lg:py-20 lg:h-svh"
		style={`background-color: ${image.mainImageConfig.bgColor};`}
	>
		<MainPageSkeleton imageData={image} />
	</div>
{/each}

<div
	class="lg:min-h-120 relative flex items-center pb-40 pt-20 lg:h-screen lg:py-0 lg:pl-0"
	id="about"
>
	<figure
		class="mx-auto flex flex-col items-center justify-center gap-x-20 gap-y-10 px-8 lg:size-full lg:flex-row lg:px-0"
	>
		<img
			src={tony}
			alt="Diseñador"
			class="lg:h-9/10 min-h-92 h-auto w-full lg:max-h-[70svh] lg:w-auto"
		/>
		<figcaption class="lg:max-w-1/2">
			<p class="font-Nexa text-vector-cream whitespace-pre-line text-sm">
				<span class="text-4xl brightness-100 [&_br]:hidden [&_em]:not-italic">
					{@html mdToHtml($i18n.t('aboutUsHead'))}
				</span>
				<span class="mt-5 block brightness-50">{$i18n.t('aboutUs')}</span>
			</p>
			<p class="font-Nexa mr-5 mt-5 text-right text-sm">Tony Quintero Gerik</p>
		</figcaption>
	</figure>
	<button
		class="text-vector-cream w-30 lg:bottom-1/10 lg:right-1/20 hover:scale-120 absolute bottom-10 right-1/2 cursor-pointer transition-transform max-lg:translate-x-1/2"
		onclick={scrollToTop}
	>
		<img src={logoWhite} alt="Vector: Interior Design" class="w-full" />
	</button>
</div>

{#each mainImages.slice(5, -1) as image (image.filename)}
	<div
		class="lg:min-h-120 max-lg:py-20 lg:h-svh"
		style={`background-color: ${image.mainImageConfig.bgColor};`}
	>
		<MainPageSkeleton imageData={image} />
	</div>
{/each}

{#each mainImages.slice(-1) as image (image.filename)}
	<NavSection {image} />
{/each}

<footer class="text-vector-cream" id="contact">
	<div class="font-Nexa relative flex items-center justify-center gap-x-5 py-20">
		<p class="border-vector-orange border-r-1 py-2 pr-5 text-2xl">{$i18n.t('contact')}</p>
		<a href="mailto:contact@vectorinterior.design" class="py-5">contact@vectorinterior.design</a>
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
