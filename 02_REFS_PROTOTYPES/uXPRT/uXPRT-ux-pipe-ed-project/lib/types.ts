export type NavItem = {
  title: string;
  href: string;
  description?: string;
};

export type MainNavItem = NavItem;

export type SidebarNavItem = {
  title: string;
  href?: string;
  items?: SidebarNavItem[];
};

export interface Document {
  title: string;
  description: string;
  icon?: string;
  href: string;
  content: string;
}

export interface Module {
  id: string;
  title: string;
  description: string;
  documents: Document[];
  coverImage?: string;
}

export interface UserProgress {
  completedModules: string[];
  completedDocuments: string[];
}