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
    const baseURL = 'https://vectorinterior.design/';
    const langs = ['en', 'es']
    return new Response(
        `
		<?xml version="1.0" encoding="UTF-8" ?>
		<urlset 
        xmlns="https://www.sitemaps.org/schemas/sitemap/0.9" 
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" 
        xmlns:xhtml="https://www.w3.org/TR/xhtml1"
        >
        ${langs.map(lang => {
            const langUrl = `${baseURL}${lang}`;
            return ` 
            <url>
              <loc>${langUrl}</loc>
                <changefreq>yearly</changefreq>
                <priority>1.0</priority>
            </url>
            <url>
              <loc>${langUrl}/esculturas</loc>
                <changefreq>yearly</changefreq>
                <priority>0.7</priority>
            </url>
            <url>
                <loc>${langUrl}/proyectos</loc>
                <changefreq>yearly</changefreq>
                <priority>0.8</priority>
            </url>
            ${projects.map(project => {
                const projectUrl = `${langUrl}/proyectos/${project.id}`;
                return `
                    <url>
                        <loc>${projectUrl}</loc>
                        <changefreq>yearly</changefreq>
                        <priority>0.5</priority>
                        <xhtml:link rel="alternate" hreflang="${lang}" href="${projectUrl}" />
                        ${project.spaces.map(space => {
                    return space.images.map(image => {
                        return ['descriptionEn', 'descriptionEs'].map((_, i) => {
                            return `
                                <image:image>
                                    <image:loc>https:${image.imageUrl}</image:loc>
                                    ${(i === 0 && image.descriptionEn) || (i === 1 && image.descriptionEs) ?
                                    `<image:caption>${i === 0 ? image.descriptionEn : image.descriptionEs}</image:caption>`
                                    : ''}
                                    </image:image>
                                        `.trim();
                        }).join('');
                    }).join('');
                }).join('')}
                    </url>
                `.trim();
            })
                }
            `
        }).join('')}
           
		</urlset>
        `.trim(),
        {
            headers: {
                'Content-Type': 'application/xhtml+xml'
            }
        }
    );
}
