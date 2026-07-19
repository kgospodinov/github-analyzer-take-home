import { Component, Input } from '@angular/core';

@Component({
    selector: 'app-repo-card',
    standalone: false,
    templateUrl: './repo-card.component.html',
    styleUrl: './repo-card.component.css'
})
export class RepoCardComponent {
    @Input() name!: string;
    @Input() language: string | null = null;
}
