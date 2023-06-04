export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "AskWizz",
  description:
    "Enterprise search for your knowledge bases, documents, and more.",
  mainNav: [
    {
      title: "Home",
      href: "/",
    },
    {
      title: "Connections",
      href: "/connections",
    },
    {
      title: "New connection",
      href: "/new-connection",
    },
  ],
  links: {
    twitter: "https://twitter.com/shadcn",
    github: "https://github.com/shadcn/ui",
    docs: "https://ui.shadcn.com",
  },
};
