<script lang="ts">
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import logo from '$lib/images/logo.svg';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();
	const projects = data.projects;

	onMount(() => {
		const arrow = document.getElementById('arrow')!;
		arrow.addEventListener('transitionend', (e: TransitionEvent) => {
			arrow.classList.add('animate');
			e.target?.removeEventListener('transitionend', null);
		});

		setTimeout(() => {
			arrow.classList.add('showing');
		}, 3000);

		const arrowLimit = document.getElementById('arrowLimit');

		if (arrowLimit) {
			const observer = new IntersectionObserver((entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						if (arrow.classList.contains('showing')) {
							arrow.classList.remove('showing');
							arrow.classList.remove('hiding');
							setTimeout(() => arrow.remove(), 100);
						} else arrow.remove();

						observer.disconnect();
					}
				});
			});

			observer.observe(arrowLimit);
		}
	});
</script>

<header class="bg-vector-grey absolute top-0 z-10 flex h-24 w-full justify-center p-5 lg:static">
	<a href="/" class="h-full transition-transform hover:scale-125">
		<img src={logo} alt="Vector: Interior Design" class="h-full" />
	</a>
</header>

<div class="h-dvh snap-y snap-mandatory overflow-y-scroll lg:hidden">
	{#each projects as project, i (project.id)}
		{#if project.thumbnail}
			<div class="flex h-dvh snap-center items-center justify-center bg-black text-white">
				<div class="relative top-16">
					<a href={`/proyectos/${project.id}`} class="flex flex-col gap-6 px-8">
						<img
							src={`${PUBLIC_imagesUrl}${project.thumbnail.filename}`}
							alt={project.thumbnail.altTextEs}
						/>
						<p class="font-Agency-FB text-[1.7rem]">{project.name}</p>
					</a>
				</div>
				{#if i === 1}
					<div id="arrowLimit" inert></div>
				{/if}
			</div>
		{/if}
		{#if i === 0}
			<div id="arrow" inert></div>
		{/if}
	{/each}
</div>

<div class="hidden flex-wrap items-center justify-center lg:flex">
	{#each projects as project, i (project.id)}
		<div
			class={`flex basis-1/3 ${i <= 2 ? 'h-[calc(100svh-6rem)]' : 'h-screen'} w-fit flex-col justify-center self-center justify-self-center`}
		>
			<a
				href={`/proyectos/${project.id}`}
				class="m-auto flex h-2/3 flex-col items-start gap-y-2 transition-transform hover:scale-110"
			>
				<img
					src={`${PUBLIC_imagesUrl}${project.thumbnail.filename}`}
					alt={project.thumbnail.altTextEs}
					class="h-full"
				/>
				<p class="font-Agency-FB ml-2 text-xl text-white">{project.name}</p>
			</a>
		</div>
	{/each}
</div>

<style>
	#arrow {
		position: absolute;
		left: 50%;
		opacity: 0;
		bottom: 10%;
		transform: translate(-50%, 0) rotate(45deg);
		height: 20px;
		width: 20px;
		border-bottom: 5px solid white;
		border-right: 5px solid white;
		border-radius: 2px;
		transition: all 2s ease-out;
	}

	:global #arrow.showing {
		opacity: 1;
		bottom: 5%;
	}

	:global #arrow.hiding {
		transition: opacity 0.1s;
		opacity: 0;
	}

	:global #arrow.animate {
		animation-name: arrowHover;
		animation-duration: 1s;
		animation-direction: alternate;
		animation-iteration-count: infinite;
	}

	@keyframes arrowHover {
		from {
			bottom: 5%;
		}
		to {
			bottom: 3%;
		}
	}
</style>
