import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User, UserPayload } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000/api/users';

  getUsers(search?: string): Observable<User[]> {
    let params = new HttpParams();
    if (search) {
      params = params.set('search', search);
    }
    return this.http.get<User[]>(this.baseUrl, { params });
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/${id}`);
  }

  createUser(payload: UserPayload): Observable<User> {
    return this.http.post<User>(this.baseUrl, payload);
  }

  updateUser(id: number, payload: UserPayload): Observable<User> {
    return this.http.put<User>(`${this.baseUrl}/${id}`, payload);
  }

  deleteUser(id: number): Observable<unknown> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }
}