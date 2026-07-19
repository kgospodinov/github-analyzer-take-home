import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { RepoCardComponent } from './repo-card/repo-card.component';
import { TechCardComponent } from './tech-card/tech-card.component';
import { StatCardComponent } from './stat-card/stat-card.component';

@NgModule({
    declarations: [AppComponent, RepoCardComponent, TechCardComponent, StatCardComponent],
    imports: [
        BrowserModule,
        FormsModule,
        HttpClientModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})

export class AppModule{}