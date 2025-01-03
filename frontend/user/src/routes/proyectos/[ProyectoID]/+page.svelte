<script lang="ts">
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import '$lib/styles/markdown.css';
	import mdToHtml from '$lib/utilities/markdown';
	import * as enums from '$lib/utilities/enums';

	const { data }: { data: PageData } = $props();
	const obraData = data.obraData;
</script>

<div class="min-h-screen bg-black">
	<header class="bg-vector-grey sticky top-0 z-10 mb-12 p-5">
		<div class="flex items-center justify-around">
			<img src={logo} alt="logo" class="w-1/3" />
			<p class="font-Agency-FB tracking-widest" style="word-spacing: 0.2rem;">
				Obras únicas y exclusivas
			</p>
		</div>
	</header>

	{#each obraData.ambientes.slice(0, 1) as ambiente (ambiente.id)}
		<img
			src={`${PUBLIC_imagesUrl}${ambiente.images.at(0)?.filename}`}
			alt={ambiente.images.at(0)?.altText}
			class:px-8={ambiente.images.shift()?.phoneConfig.alignment !== enums.Alignment.Sangrar}
		/>

		<div class="mx-8 my-12 text-white">
			<h1 class="font-Agency-FB border-b-vector-orange my-2 border-b-2 pb-2 indent-1 text-4xl">
				{obraData.name}
			</h1>
			<p class="font-Arial text-right text-sm">Área: {obraData.area} metros cuadrados</p>
			<p class="white my-6 text-justify indent-4">{obraData.description}</p>
		</div>
	{/each}

	<div>
		{#each obraData.ambientes.slice(0) as ambiente (ambiente.id)}
			{#each ambiente.images as image (image.filename)}
				{#if image.filename !== obraData.thumbnail?.filename}
					<div
						class={`border-vector-orange my-12 gap-2 ${image.phoneConfig.borders.n && 'border-t-2 pt-5'} ${image.phoneConfig.borders.s && 'border-b-2 pb-5'} ${image.phoneConfig.borders.e && 'border-r-2 pr-5'} ${image.phoneConfig.borders.o && 'border-l-2 pl-5'}`}
						class:mx-8={image.phoneConfig.alignment !== enums.Alignment.Sangrar}
						class:flex={image.phoneConfig.descriptionPos}
						class:flex-row={image.phoneConfig.descriptionPos === enums.Direction.O}
						class:flex-row-reverse={image.phoneConfig.descriptionPos === enums.Direction.E}
						class:flex-col={image.phoneConfig.descriptionPos === enums.Direction.N}
						class:flex-col-reverse={image.phoneConfig.descriptionPos === enums.Direction.S}
					>
						{#if image.description && image.phoneConfig.descriptionPos}
							<div class="markdownDescription text-lg">
								{@html mdToHtml(image.description)}
							</div>
						{/if}
						<img
							src={`${PUBLIC_imagesUrl}${image.filename}`}
							alt={image.altText}
							class={`${[enums.Alignment.Derecha, enums.Alignment.Izquierda].includes(image.phoneConfig.alignment) ? 'w-2/3' : ''}`}
							class:ml-auto={image.phoneConfig.alignment === enums.Alignment.Derecha}
							class:mr-auto={image.phoneConfig.alignment === enums.Alignment.Izquierda}
						/>
					</div>
				{/if}
			{/each}
		{/each}
	</div>
</div>
