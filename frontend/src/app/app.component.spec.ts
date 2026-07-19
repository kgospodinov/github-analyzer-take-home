import { TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { Subject, of, throwError } from 'rxjs';

import { AppComponent } from './app.component';
import { GithubService } from './github.service';

describe('AppComponent.search', () => {
    let githubServiceSpy: { getUser: ReturnType<typeof vi.fn> };

    beforeEach(() => {
        githubServiceSpy = { getUser: vi.fn() };

        TestBed.configureTestingModule({
            declarations: [AppComponent],
            imports: [FormsModule],
            providers: [{ provide: GithubService, useValue: githubServiceSpy }],
        });
    });

    function createComponent() {
        return TestBed.createComponent(AppComponent).componentInstance;
    }

    it('shows an error and does not call the service when the username is empty', () => {
        const component = createComponent();
        component.githubUsername = '';

        component.search();

        expect(component.error()).toBe('Please enter a GitHub username.');
        expect(githubServiceSpy.getUser).not.toHaveBeenCalled();
    });

    it('sets loading while the request is in flight', () => {
        const subject = new Subject();
        githubServiceSpy.getUser.mockReturnValue(subject);
        const component = createComponent();
        component.githubUsername = 'test-github-user';

        component.search();

        expect(component.loading()).toBe(true);
    });

    it('sets data and clears loading on success', () => {
        const response = { followers_count: 5 };
        githubServiceSpy.getUser.mockReturnValue(of(response));
        const component = createComponent();
        component.githubUsername = 'test-github-user';

        component.search();

        expect(githubServiceSpy.getUser).toHaveBeenCalledWith('test-github-user');
        expect(component.data()).toEqual(response);
        expect(component.loading()).toBe(false);
        expect(component.error()).toBe('');
    });

    it('sets the error message from the response and clears loading on failure', () => {
        githubServiceSpy.getUser.mockReturnValue(throwError(() => ({ error: { detail: 'User not found' } })));
        const component = createComponent();
        component.githubUsername = 'does-not-exist';

        component.search();

        expect(component.error()).toBe('User not found');
        expect(component.loading()).toBe(false);
        expect(component.data()).toBeNull();
    });

    it('falls back to a generic error message when none is provided', () => {
        githubServiceSpy.getUser.mockReturnValue(throwError(() => ({})));
        const component = createComponent();
        component.githubUsername = 'test-github-user';

        component.search();

        expect(component.error()).toBe('Something went wrong.');
    });
});
