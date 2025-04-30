import graphql from "$lib/utilities/api";

interface Projects {
    id: number
    spaces: {
        images: {
            imageUrl: string
            descriptionEs: string
            descriptionEn: string
        }[]
    }[]
}


const langs = ['en', 'es'];
const baseURL = 'https://vectorinterior.design/';
const langURL = `${baseURL}${langs[0]}`;

// Generates the `xhtml:link` tags for all languages for the given url relative to the base.
// Example: For url `https://vectorinterior.design/en/proyectos` pass only `/proyectos`
function generateLocalizedTags(relUrl: string): string {
    let tags = langs.map(lang => {
        return `<xhtml:link rel="alternate" hreflang="${lang}" href="${baseURL}${lang}${relUrl}"/>`;
    }).join('\n');

    return tags;
}

export async function GET({ fetch }) {
    const query = `
        query projects {
            projects {
                id
                spaces {
                    images {
                        imageUrl
                        descriptionEs
                        descriptionEn
                    }
                }
            }
        }
    `;

    const projects: Projects[] = (await graphql(query, {}, fetch)).projects;

    return new Response(
        `
<?xml version="1.0" encoding="UTF-8" ?>
		<urlset 
        xmlns="https://www.sitemaps.org/schemas/sitemap/0.9" 
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
        <url>
            <loc>${langURL}</loc>
            ${langs.map(lang => {
            // Not using `generateLocalizedUrl` here since its the base path
            return `<xhtml:link rel="alternate" hreflang="${lang}" href="${baseURL}${lang}"/>`
        }).join('\n')}
            <changefreq>yearly</changefreq>
            <priority>1.0</priority>
        </url>
        <url>
            <loc>${langURL}/esculturas</loc>
            ${generateLocalizedTags("/esculturas")}
            <changefreq>yearly</changefreq>
            <priority>0.7</priority>
        </url>
        <url>
            <loc>${langURL}/proyectos</loc>
            ${generateLocalizedTags("/proyectos")}
            <changefreq>yearly</changefreq>
            <priority>0.8</priority>
        </url>
           
        ${projects.map(project => {
            const projectUrl = `${langURL}/proyectos/${project.id}`;
            return `
                    <url>
                        <loc>${projectUrl}</loc>
                        ${generateLocalizedTags(`/proyectos/${project.id}`)}
                        <changefreq>yearly</changefreq>
                        <priority>0.5</priority>

                        ${project.spaces.map(space => {
                return space.images.map(image => {
                    return ['descriptionEn', 'descriptionEs'].map((lang, i) => {
                        return `
                                <image:image>
                                    <image:loc>https:${image.imageUrl}</image:loc>
                                    ${(i === 0 && image.descriptionEn) || (i === 1 && image.descriptionEs) ?
                                `<image:caption xml:lang="${lang}">${i === 0 ? image.descriptionEn : image.descriptionEs}</image:caption>`
                                : ''}
                                    </image:image>
                                        `.trim();
                    }).join('\n');
                }).join('\n');
            }).join('\n')}
                    </url>
                `.trim();
        })
            }
		</urlset>
        `.trim(),
        {
            headers: {
                'Content-Type': 'application/xhtml+xml'
            }
        }
    );
}
