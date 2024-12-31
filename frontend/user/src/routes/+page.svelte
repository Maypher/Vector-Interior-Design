<script lang="ts">
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import logoWhite from '$lib/images/logo white.svg';
	import type { PageData } from './$types';
	import tony from '$lib/images/tony.jpg';
	import tonyContact from '$lib/images/contact.jpg';
	import { Direction } from '$lib/utilities/enums';

	interface Borders {
		n: boolean;
		s: boolean;
		e: boolean;
		o: Boolean;
	}

	interface mainImageData {
		filename: string;
		altText: string;
		mainImageConfig: {
			description?: string;
			descriptionPos?: 'N' | 'S' | 'E' | 'O';
			logoPos?: 'N' | 'S' | 'E' | 'O';
			descriptionFontSize: string;
			descriptionFont: string;
			descriptionAlignment: string;
			overflow?: boolean;
			imageBorders: Borders;
			logoBorders: Borders;
		};
	}

	const { data }: { data: PageData } = $props();
	const mainImages: mainImageData[] = data.mainImages;
</script>

{#snippet mainImage(imageData: mainImageData)}
	<div
		class="mt-10 flex flex-col gap-10"
		class:flex={imageData.mainImageConfig.logoPos}
		class:flex-col={imageData.mainImageConfig.logoPos === Direction.N}
		class:flex-col-reverse={imageData.mainImageConfig.logoPos === Direction.S}
		class:flex-row-reverse={imageData.mainImageConfig.logoPos === Direction.E}
	>
		{#if imageData.mainImageConfig.logoPos}
			<div
				class={`m-auto w-10/12 border-[#ff4800] ${imageData.mainImageConfig.logoBorders.n ? 'border-t-2 pt-10' : ''} ${imageData.mainImageConfig.logoBorders.s ? 'border-b-2 pb-10' : ''} ${imageData.mainImageConfig.logoBorders.e ? 'border-r-2 pr-10' : ''} ${imageData.mainImageConfig.logoBorders.o ? 'border-l-2 pl-10' : ''}`}
			>
				<img src={symbol} alt="symbol" class="mx-auto w-20" />
			</div>
		{/if}
		<div
			class="gap-10"
			class:flex={imageData.mainImageConfig.descriptionPos && imageData.mainImageConfig.description}
			class:flex-col={imageData.mainImageConfig.descriptionPos === Direction.N}
			class:flex-col-reverse={imageData.mainImageConfig.descriptionPos === Direction.S}
			class:flex-row-reverse={imageData.mainImageConfig.descriptionPos === Direction.E}
		>
			{#if imageData.mainImageConfig.description}
				<div class="m-auto w-10/12">
					{#each imageData.mainImageConfig.description.split('\n\n') as paragraph, i}
						<p
							class={`size-fit indent-2 text-white ${imageData.mainImageConfig.descriptionAlignment}`}
							style={`font-family: ${imageData.mainImageConfig.descriptionFont}; 
							font-size: ${imageData.mainImageConfig.descriptionFontSize}rem; line-height: 1.8;`}
						>
							{paragraph}
						</p>
						{#if i !== 2}<br />{/if}
					{/each}
				</div>
			{/if}
			<img
				src={`${PUBLIC_imagesUrl}${imageData.filename}`}
				alt={imageData.altText}
				class={`m-auto border-[#ff4800] ${!imageData.mainImageConfig.overflow ? 'w-10/12' : ''} ${imageData.mainImageConfig.imageBorders.n ? 'border-t-2 pt-10' : ''} ${imageData.mainImageConfig.imageBorders.s ? 'border-b-2 pb-10' : ''} ${imageData.mainImageConfig.imageBorders.e ? 'border-r-2 pr-10' : ''} ${imageData.mainImageConfig.imageBorders.o ? 'border-l-2 pl-10' : ''}`}
			/>
		</div>
	</div>
{/snippet}

<div class="flex h-screen flex-col justify-between bg-black">
	<header class="flex h-1/4 items-center justify-between p-5">
		<img src={logo} alt="" class="m-auto h-fit w-72" id="logo" />
	</header>

	<div>
		<p class="text-center text-4xl text-white" style="font-family: Agency-FB; line-height: 3rem">
			{`Trazando líneas con
				 dirección, pasión y estilo.`}
		</p>
	</div>
	{#each mainImages.slice(0, 1) as image (image.filename)}
		{@render mainImage(image)}
	{/each}
</div>

<div>
	{#each mainImages.slice(1, 6) as image (image.filename)}
		{@render mainImage(image)}
	{/each}
</div>

<div class="my-10 flex flex-col bg-black">
	<img src={tony} alt="Diseñador" class="ml-auto w-5/6" />
	<p class="my-8 px-8 text-justify indent-3 text-lg text-white">
		{`De lo sublime a lo majestuoso, el límite de este  este diseñador es infinito. Definiendo la personalidad de sus clientes es capaz de convertir los espacios más simples en obras únicas y exclusivas, logrando un impacto visual certero y a veces hasta inimaginable.`}
	</p>
	<img src={logoWhite} alt="Logo white" class="mx-auto my-6 w-44" />
</div>

<div>
	{#each mainImages.slice(6, 8) as image (image.filename)}
		{@render mainImage(image)}
	{/each}
</div>

<div
	class="m-auto my-20 w-10/12 border-2 border-[#ff4800] py-8 text-center font-[Bahnschrift] text-2xl font-thin tracking-[0.5rem] text-white"
	style="word-spacing: 1rem;"
>
	Interior Design
</div>

<div>
	{#each mainImages.slice(8, -1) as image (image.filename)}
		{@render mainImage(image)}
	{/each}
</div>

<div class="relative mt-10 flex h-screen flex-col overflow-hidden py-4">
	<div class="absolute right-40 -z-10 flex w-20 flex-col" id="pencil">
		<img src={symbol} alt="Logo" />
	</div>
	<div class="mt-44 w-full">
		{@render mainImage(mainImages.at(-1)!)}
	</div>
	<div class="my-12 flex flex-col gap-32">
		<p class="ml-auto mr-14 w-fit text-4xl text-white" style="font-family: Agency-FB;">
			Esculturas
		</p>
		<p class="ml-auto mr-56 w-fit text-4xl text-white" style="font-family: Agency-FB;">Proyectos</p>
	</div>
</div>

<div class="flex h-screen flex-col justify-between">
	<div class="flex justify-end">
		<div class="relative left-2 z-10 flex flex-col justify-end gap-4">
			<p
				class="size-fit text-white"
				style="font-family: Agency-FB; font-size: 5rem; line-height: 4rem"
			>
				CON
			</p>
			<p
				class="relative left-[4.6rem] size-fit text-white"
				style="font-family: Agency-FB; font-size: 5rem; line-height: 4rem;"
			>
				TAC
			</p>
		</div>
		<div class="relative flex flex-col items-center">
			<img src={tonyContact} alt="Contacto" style="width: 65vw" />
			<div class="absolute -bottom-20">
				<p
					class="block size-fit text-[5rem] text-white"
					style="font-family: Agency-FB; line-height: 4rem;"
				>
					TO
				</p>
				<p class="absolute -bottom-1 right-16 text-white">contact@vector.com</p>
			</div>
		</div>
	</div>
	<footer class="flex h-2/5 items-center justify-center">
		<img src={logoWhite} alt="Logo white" class="w-1/2" />
	</footer>
</div>

<style>
	@font-face {
		font-family: 'Agency-FB';
		font-style: normal;
		font-weight: 400;
		src: url('/fonts/agency-fb.ttf');
	}

	@font-face {
		font-family: 'Bahnschrift';
		font-style: normal;
		font-weight: 100;
		src: url('/fonts/bahnschrift.ttf');
	}

	:global(body) {
		background-color: black;
	}

	header {
		background-color: #e6e6e6;
	}

	p {
		font-family: Arial, Helvetica, sans-serif;
		font-weight: normal;
		line-height: 1.5rem;
		white-space: pre-line;
	}

	#pencil {
		animation: pencil-draw 2s ease-in-out;
	}

	#pencil::after {
		position: relative;
		content: '';
		width: 2px;
		height: 80vh;
		background-color: #ff4800;
		border-radius: 50px;
		margin: auto;
	}

	@media (max-width: 500px) {
		#pencil::after {
			top: -1rem;
		}
	}

	@keyframes pencil-draw {
		from {
			top: 100%;
		}

		to {
			top: 0;
		}
	}

	.grid > * {
		border: 2px solid red;
	}
</style>
