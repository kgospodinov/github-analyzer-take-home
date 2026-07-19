import { Component, Input } from '@angular/core';

@Component({
    selector: 'app-tech-card',
    standalone: false,
    templateUrl: './tech-card.component.html',
    styleUrl: './tech-card.component.css'
})
export class TechCardComponent {
    @Input() tech!: string;
}
