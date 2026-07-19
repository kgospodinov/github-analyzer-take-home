import { Component, signal } from '@angular/core';
import { GithubService } from './github.service';


@Component({
    selector: 'app-root',
    standalone: false,
    templateUrl: './app.component.html'
})

export class AppComponent {

    githubUsername = '';
    data = signal<any>(null);
    error = signal('');
    loading = signal(false);

    constructor(private githubService: GithubService) {}

    search() {
        this.error.set('');
        this.data.set(null);

        if (!this.githubUsername) {
            this.error.set('Please enter a GitHub username.');
            return;
        }

        this.loading.set(true);

        this.githubService.getUser(this.githubUsername).subscribe({
            next: (response) => {
                this.data.set(response);
                this.loading.set(false);
            },
            error: (err) => {
                this.error.set(err?.error?.detail || 'Something went wrong.');
                this.loading.set(false);
            }
        });
    }

}
