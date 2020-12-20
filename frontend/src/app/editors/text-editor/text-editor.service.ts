import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, Subject, asapScheduler, pipe, of, from, interval, merge, fromEvent } from 'rxjs';
import 'rxjs/add/operator/catch';
import {API_URL} from '../../../environments/environment';
import { catchError, retry } from 'rxjs/operators';
//import {AnnotatedImage} from "./annotation.model"

@Injectable()
export class RecommenderApiService {
  constructor(private http: HttpClient) {}

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }
  // Get Patient by her id
  recommendImages(text:string, num_images:number): Observable<any> {
    return this.http.get<any>(`${API_URL}/recommend_images?text=${text}&num_images=${num_images}`)
      .pipe(
        catchError(err => {
          console.log(err);
          return of(null);
            })
      );
  }
}
