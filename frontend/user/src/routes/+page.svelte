<script lang="ts">
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import logoWhite from '$lib/images/logo white.svg';
	import type { PageData } from './$types';
	import tony from '$lib/images/tony.jpg';
	import tonyContact from '$lib/images/contact.jpg';

	const { data }: { data: PageData } = $props();
	console.log(data.obras.obras.at(-1));
</script>

<div class="flex h-screen flex-col bg-black">
	<header class="flex items-center justify-between p-5" style="height: 35%;">
		<img src={logo} alt="" class="m-auto h-fit w-72" id="logo" />
	</header>

	<div class="flex basis-full flex-col">
		<div class="flex basis-full items-center justify-center">
			<p
				class="text-center text-4xl text-white sm:block"
				style="font-family: Agency-FB; line-height: 3rem"
			>
				{`Trazando líneas con
				 dirección, pasión y estilo.`}
			</p>
		</div>
		{#if data.obras.obras[0]}
			{#if data.obras.obras[0].thumbnail}
				<img
					src={`${PUBLIC_imagesUrl}${data.obras.obras[0].thumbnail?.filename}`}
					alt={data.obras.obras[0].thumbnail.altText}
				/>
			{/if}
		{/if}
	</div>
</div>

<div class="flex min-h-screen flex-col bg-black">
	<div class="flex basis-full flex-col">
		<div class="flex basis-full items-center justify-center">
			<div class="p-8 text-justify indent-3 text-lg text-white">
				<p>
					{'Mediante los atributos del diseñador el glamour y el buen gusto logran la fusión perfecta entre arquitectura, artes gráficas y diseño interior marcando sin duda alguna distinción'}
				</p>
				<br />
				<p>
					{`El punto de partida para sus creaciones es una inerte obra gris que finalmente entrega convertida en una obra de arte llena de espacios confortables totalmente decorados y listos para su disfrute.`}
				</p>
				<br />
				<p>
					{'Especializado en imagen corporativa y diseño interior, con una experiencia laboral de más de 20 años, este artista presta un servicio integral, dedicado al diseño y decoración de viviendas, oficinas y espacios comerciales.'}
				</p>
			</div>
		</div>
		{#if data.obras.obras[1]}
			{#if data.obras.obras[1].thumbnail}
				<img
					src={`${PUBLIC_imagesUrl}${data.obras.obras[1].thumbnail.filename}`}
					alt={data.obras.obras[1].thumbnail.altText}
				/>
			{/if}
		{/if}
	</div>
</div>

{#each data.obras.obras.slice(2, 6) as obra}
	<div class="m-auto flex min-h-screen w-10/12 flex-col bg-black">
		<div class="m-auto">
			<img src={symbol} alt="symbol" class="mx-auto w-20" />
		</div>
		<div>
			<img
				src={`${PUBLIC_imagesUrl}${obra.thumbnail.filename}`}
				alt={obra.thumbnail.altText}
				class="border-b-2 pb-16"
				style="border-color: #FF4800;"
			/>
		</div>
	</div>
{/each}

<div class="mt-16 flex flex-col bg-black">
	<img src={tony} alt="Diseñador" class="ml-auto w-5/6" />
	<p class="my-8 px-8 text-justify indent-3 text-lg text-white">
		{`De lo sublime a lo majestuoso, el límite de este  este diseñador es infinito. Definiendo la personalidad de sus clientes es capaz de convertir los espacios más simples en obras únicas y exclusivas, logrando un impacto visual certero y a veces hasta inimaginable.`}
	</p>
	<img src={logoWhite} alt="Logo white" class="mx-auto my-6 w-44" />
</div>

<div>
	{#each data.obras.obras.slice(6, -1) as obra, i}
		<div class="flex flex-col bg-black">
			{#if i !== 0 && i !== 2}
				<div class="m-auto w-10/12 border-b-2 pb-16" style="border-color: #FF4800;">
					<img src={symbol} alt="symbol" class="mx-auto w-20" />
				</div>
			{/if}
			<div class={`my-16 ${i === 4 ? 'm-auto w-10/12' : ''}`}>
				<img src={`${PUBLIC_imagesUrl}${obra.thumbnail?.filename}`} alt={obra.thumbnail?.altText} />
			</div>
			{#if i === 1}
				<div class="mx-auto my-6 w-9/12 border-2 py-8" style="border-color: #FF4800;">
					<p
						style="font-family: Bahnschrift; word-spacing: 0.5rem; letter-spacing: 0.5rem;"
						class="m-auto text-center text-2xl text-white"
					>
						Interior Design
					</p>
				</div>
			{/if}
			{#if i === 3}
				<div class="m-auto mb-16 w-10/12">
					<p
						class="text-center text-3xl text-white"
						style="font-family: Agency-FB; line-height: 3rem;"
					>
						{`"Los elementos decorativos
						son parte integral de 
						toda decoración"`}
					</p>
				</div>
			{/if}
		</div>
	{/each}
</div>

<div class="relative flex h-screen flex-col overflow-hidden py-4">
	<div class="absolute right-40 -z-10 flex w-20 flex-col" id="pencil">
		<img src={symbol} alt="Logo" />
	</div>
	<div class="mt-44 w-full">
		<img
			src={`${PUBLIC_imagesUrl}${data.obras.obras.at(-1).thumbnail?.filename}`}
			alt={data.obras.obras.at(-1).thumbnail?.altText}
		/>
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
				<p class="absolute bottom-0 right-16 text-white">contacto@vector.com</p>
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
		font-weight: 400;
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
