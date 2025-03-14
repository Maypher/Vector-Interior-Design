<script lang="ts">
	import { websiteUrl } from '$lib/utilities/constants';
	import Head from '$lib/components/Head.svelte';
	import logo from '$lib/images/logo.svg';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';

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

	const i18n = getI18n();
</script>

<Head
	title={$i18n.language === 'es' ? 'Proyectos' : 'Projects'}
	description={$i18n.language === 'es' ? '' : ''}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en/proyectos`}
	alternateEs={`${websiteUrl}/es/proyectos`}
	ogTitle={$i18n.language === 'es'
		? 'Vector: Interior Design (Proyectos)'
		: 'Vector: Interior Design (Projects)'}
	ogDescription={$i18n.language === 'es' ? '' : ''}
	imageUrl={projects.at(0).thumbnail.imageUrl}
/>

<ul class="h-svh snap-y snap-mandatory overflow-y-scroll lg:hidden">
	{#each projects as project, i (project.id)}
		{#if project.thumbnail}
			<li class="relative flex h-full snap-center items-center justify-center bg-black text-white">
				<div class="absolute bottom-0 flex h-[calc(100%-6rem)] flex-col justify-center">
					<a
						href={`/${$i18n.language}/proyectos/${project.id}`}
						class="flex h-3/4 flex-col justify-center gap-6 px-8"
					>
						<figure class="h-full">
							<img
								src={project.thumbnail.imageUrl}
								alt={project.thumbnail.altText}
								class="h-full object-cover"
							/>
							<figcaption>
								<p class="font-Agency-FB text-[1.7rem]">{project.name}</p>
							</figcaption>
						</figure>
					</a>
				</div>
				{#if i === 1}
					<div id="arrowLimit" inert></div>
				{/if}
			</li>
		{/if}
		{#if i === 0}
			<div id="arrow" inert></div>
		{/if}
	{/each}
</ul>

<ul class="hidden flex-wrap items-center justify-evenly lg:flex">
	{#each projects as project, i (project.id)}
		<li
			class={`flex basis-1/3 ${i <= 2 ? 'h-[calc(100svh-5rem)]' : 'h-screen'} min-h-96 w-fit flex-col justify-center self-center justify-self-center`}
		>
			<a
				href={`/${$i18n.language}/proyectos/${project.id}`}
				class="m-auto flex h-2/3 flex-col items-start gap-y-2 transition-transform hover:scale-110"
			>
				<figure class="h-full">
					<img src={project.thumbnail.imageUrl} alt={project.thumbnail.altText} class="h-full" />
					<figcaption>
						<p class="font-Nexa my-5 text-[0.6rem] font-extralight" style="letter-spacing: 0.1rem;">
							{project.name}
						</p>
					</figcaption>
				</figure>
			</a>
		</li>
	{/each}
</ul>

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
