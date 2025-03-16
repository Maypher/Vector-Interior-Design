<script lang="ts">
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import { type Snippet } from 'svelte';
	import cookies from 'js-cookie';
	import type { PageData } from './$types';
	import { afterNavigate } from '$app/navigation';
	import logo from '$lib/images/logo.svg';

	let { children }: { data: PageData; children: Snippet } = $props();
	const i18n = getI18n();

	afterNavigate(() => {
		const selectedLang = $i18n.language;
		const currentLang = page.url.pathname.split('/').at(1);

		if (currentLang !== selectedLang) {
			const redirectTo = `/${selectedLang}/${getRemainingUrl()}`;
			location.replace(redirectTo);
		}
	});

	async function changeLanguage(lang: string) {
		menuOpen = false; // Close menu for lg devices and smaller. Doesn't have any effect on xl devices
		cookies.set('lang', lang, { path: '/', httpOnly: false });
		const redirectTo = `/${lang}/${getRemainingUrl()}`;
		location.replace(redirectTo);
	}

	function getRemainingUrl(): string {
		// Removing the first element since the url is /en/something and the first element is an empty string
		const splitURL = page.url.pathname.split('/').slice(1);
		const remainingURL = splitURL.slice(1);

		return remainingURL.join('/');
	}

	let menuOpen: boolean = $state(false);

	function openMenu() {
		menuOpen = !menuOpen; // Toggle the menu state

		// If the menu was opened then add an event listener to close it when clicking outside it
		if (menuOpen) {
			const menuElement = document.getElementById('menu')!;

			// Using setTimeout with delay 0 because since the 'click' event
			// triggers with the click to open the menu this delays it to the next
			// cycle which is enough to not trigger it automatically.
			setTimeout(() => {
				document.addEventListener('click', function checkClick(e) {
					const clickedElement = e.target as Node;
					const clickedUrl = clickedElement.nodeName === 'A';
					const clickInsideMenu = menuElement.contains(clickedElement);

					// If a link in the menu or another element was clicked close it
					// Doesn't close when clicking select language on purpose
					// It's closed directly when changing language.
					if (!clickInsideMenu || clickedUrl) {
						// Remove the event listener so it doesn't affect performance
						document.removeEventListener('click', checkClick);
						menuOpen = false;
					}
				});
			}, 0);
		}
	}
</script>

{#snippet languageSelect()}
	<select
		onchange={(e) => changeLanguage((e.target as HTMLSelectElement).value)}
		class="font-Nexa xl:text-vector-black"
	>
		<option value="en" selected={$i18n.language === 'en'}>{$i18n.t('english')}</option>
		<option value="es" selected={$i18n.language === 'es'}>{$i18n.t('Spanish')}</option>
	</select>
{/snippet}

<header class="bg-vector-cream h-22 flex items-center justify-between gap-20 p-5 px-10">
	<a href={`/${$i18n.language}`} class="hover:scale-120 h-full transition-transform">
		<img src={logo} alt="Vector: Interior Design" class="h-full" />
	</a>
	<div
		class={`font-Nexa text-vector-black hidden gap-20 [&_a]:transition-colors ${page.url.pathname === `/${$i18n.language}` ? 'hidden' : 'xl:flex'}`}
	>
		<a href={`/${$i18n.language}/`} class="hover:text-vector-orange"> Página principal </a>
		<a href={`/${$i18n.language}/proyectos`} class="hover:text-vector-orange">Proyectos</a>
		<a href={`/${$i18n.language}/esculturas`} class="hover:text-vector-orange">Esculturas</a>
		<a href={`/${$i18n.language}/#about`} class="hover:text-vector-orange">Nosotros</a>
		<a href={`/${$i18n.language}/#contact`} class="hover:text-vector-orange">Contacto</a>
	</div>
	<div class="hidden xl:block">
		{@render languageSelect()}
	</div>
	<button
		class={`text-vector-black block text-4xl transition-transform ${menuOpen ? '-rotate-90' : ''} xl:hidden`}
		onclick={openMenu}
	>
		☰
	</button>
</header>
<div
	class="grid w-full text-right transition-all xl:hidden"
	id="menu"
	style={`grid-template-rows: ${menuOpen ? '1fr' : '0fr'};`}
>
	<ul
		class="font-Nexa text-vector-cream flex-col items-end gap-y-2 overflow-hidden [&>li]:p-2"
		style="letter-spacing: 0.05rem;"
	>
		<li class="before:bg-vector-orange">
			<a href={`/${$i18n.language}/#about`} class="hover-link">
				{$i18n.t('about')}
			</a>
		</li>
		<li>
			<a href={`/${$i18n.language}/proyectos`} class="hover-link">{$i18n.t('projects')}</a>
		</li>
		<li>
			<a href={`/${$i18n.language}/esculturas`} class="hover-link">{$i18n.t('sculptures')}</a>
		</li>
		<li>
			<a href={`/${$i18n.language}/#contact`} class="hover-link">
				{$i18n.t('contact')}
			</a>
		</li>
		<li>
			{@render languageSelect()}
		</li>
	</ul>
</div>
{@render children()}
