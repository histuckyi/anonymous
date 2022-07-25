
## 개요
댓글 기능이 있는 익명 게시판 및 키워드 알림 기능 구현 [for Wanted]

## 기본 환경 설정
* Database : MariaDB(v10.2)
* Framework : Flask(v2.1.3)
* Language: Python(3.10.5)

## 개발 요구 사항
- 게시판 기능
  - [x] 게시판은 제목, 내용, 작성자 이름, 비밀번호, 작성일시, 수정일시로 구성되어 있습니다. 
  - [x] 로그인 기능 없이 작성자도 입력 파라미터로 받습니다. 
  - [x] 게시판은 제목, 작성자로 검색이 가능합니다. 
  - [x] 게시글 작성, 수정, 삭제가 가능합니다. 
  - [x] 게시글 작성시에는 비밀번호를 입력받고, 수정/삭제시 입력한 비밀번호가 맞는 경우만 가능합니다. 
  - [x] 게시글에는 댓글을 작성할 수 있습니다. 
  - [x] 댓글은 내용, 작성자, 작성일시로 구성되어 있습니다. 
  - [x] 댓글의 댓글까지 작성이 가능합니다. 
  - [x] 게시물, 댓글 목록 API는 페이징 기능이 있어야 합니다. 
- 키워드 알림 기능 
  - [x] 키워드 알림 테이블은 작성자 이름, 키워드 컬럼을 포함하고 있어야 하고 편의상 작성자는 동명이인이 없다고 가정합니다. 작성자가 등록한 키워드가 포함된 게시글이나 코멘트 등록시 알림을 보내줍니다. 
  - [x] 키워드 등록/삭제 부분은 구현을 안하셔도 됩니다. 
  - [x] 알림 보내는 함수 호출하는 것으로만 하고 실제 알림 보내는 기능은 구현하지 않습니다. 

## 구현 설명
* 요구사항에 따라 게시글(Post)와 댓글(Comment)를 구현하였습니다.
* 키워드 알림 기능은 아래와 같은 절차로 알림 함수를 호출합니다.
    * pynori를 사용하여 게시글과 댓글을 등록합니다.
    * pynori를 사용하여 text로부터 키워드를 추출합니다.
    * 유저가 알림 설정한 키워드는 keyword_notification에 저장되어 있습니다. 
    * 추출한 키워드를 가지고 keyword_notification 테이블로부터 사용자의 이름을 조회하여 알림 함수를 호출합니다.
  

## 환경 세팅 방법
로컬에 직접 mariadb를 설치하고 anonymous 애플리케이션을 실행한다.  
(mariadb의 기본 포트는 4100이며, root 계정의 비밀번호는 wanted)  


#### 1. 로컬에 직접 mariadb를 설치하고 anonymous 애플리케이션을 실행
mariaDB를 설치하고 anonymous를 실행하면 자동으로 테이블 생성합니다.    
(아래 테이블은 참고용)
```
create table keyword_notification
(
    id         int auto_increment
        primary key,
    keyword    varchar(300) not null,
    name       varchar(80)  not null,
    created_at datetime     not null,
    constraint name
        unique (name)
);

create table post
(
    id         int auto_increment
        primary key,
    name       varchar(80)  not null,
    password   varchar(500) not null,
    title      varchar(200) null,
    content    text         null,
    created_at datetime     not null,
    updated_at datetime     null,
    constraint name
        unique (name)
);

create table comment
(
    id                int auto_increment
        primary key,
    post_id           int          null,
    name              varchar(80)  not null,
    parent_comment_id int          null,
    content           varchar(300) not null,
    created_at        datetime     not null,
    updated_at        datetime     null,
    constraint name
        unique (name),
    constraint comment_ibfk_1
        foreign key (post_id) references post (id)
            on delete cascade,
    constraint comment_ibfk_2
        foreign key (parent_comment_id) references comment (id)
            on delete cascade
);

create index parent_comment_id
    on comment (parent_comment_id);

create index post_id
    on comment (post_id);

```
