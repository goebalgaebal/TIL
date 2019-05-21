# Git

> Git은 분산형 버전 관리 시스템(DVCS)의 일종이다 
>
> 소스코드의 이력이 기록된다

## 기본 명령어

1. git  저장소(`repository`) 초기화

   ```bash
   $ git init
   Initialized empty Git repository in C:/Users/user/Desktop/TIL/.git/
   user@DESKTOP-P5SC8GJ MINGW64 ~/Desktop/TIL (master)
   ```

   * 원하는 폴더를 저장소로 만들게 되면, `git bash`에서는 `(master)` 라고 표기된다.
   * 그리고 숨김 폴더로 `.git/`이 생성된다.





2. commit할 목록에 담기(Staging Area)

   ```bash
   $ git add .
   ```

   * 현재 작업 공간(Working Directory/ Tree)의 변경 사항을 commit할 목록에 추가한다 `(add)`
   * `.`은 리눅스에서 현재 디렉토리(폴더)를 표기하는 방법으로, 지금 내 폴더에 있는 파일의 변경사항을 전부 추가한다는 뜻이다
   * 만일 git.md 파일만을 추가하려면, `git add git.md`로 추가할 수 있다
   * 만일 myfolder 폴더를 추가하려면, `git add myfolder/`로 폴더 내의 모든 파일을 추가할 수 있다





3. commit하기 

   ```bash
   $ git commit -m 'message'
   ```

   * commit을 할 때에는 해당하는 버전의 이력을 의미하는 메시지를 반드시 적어준다

   * message를 지금 버전을 쉽게 이해할 수 있도록 작성한다

   * commit은 현재 코드의 상태를 스냅샷 찍는 것이다





4. log 확인하기

   ```bash
   $ git log
   commit 69601dd46faf0ab05a98337744aa35fb9b3bf4cf (HEAD -> master)
   Author: goebalgaebal <email>
   Date:   Tue May 21 17:12:50 2019 +0900
   
       190521 | 마크다운 연습
   ```
   
   * 현재까지 commit된 이력을 모두 확인할 수 있다





5. **git 상태 확인하기**

   ```bash
   $ git status
   ```

   * CLI(Comman Line Interface)에서는 현재 상태를 알기 위해 반드시 명령어를 통해 확인해야한다
   * commit할 목록에 담겨 있는지, untracked 인지, commit할 내역이 없는지 등등 다양한 정보를 알려준다





## 원격 저장소 활용하기

1. 원격 저장소(remote repository) 등록하기

   ```bash
   $ git remote add origin _____경로______
   ```

   * 원격 저장소(`remote`)를 등록(`add`)한다. `origin` 이라는 이름으로 `경로` 를!
   * 최초에 한번만 등록하면 된다
   * 아래의 명령어로 현재 등록된 원격 저장소를 확인할 수 있다

   ```bash
   $ git remote -v
   origin  https://github.com/goebalgaebal/TIL.git (fetch)
   origin  https://github.com/goebalgaebal/TIL.git (push)
   ```





2. 원격 저장소에 올리기(`push`)

   ```bash
   $ git push origin master 
   ```

   * `git` ! 올려줘(`push`) `origin` 이라는 이름의 원격저장소에 `master` 로!





3. 원격 저장소로 부터 가져오기(`pull`)

   ```bash
   $ git pull origin master
   ```





## 원격 저장소 복제(Clone)하기

```bash
$ git clone ____경로____
```

* 다운 받기를 원하는 폴더에서 `git bash` 를 열고 위의 명령어를 입력한다
* 경로는 `github` 에서 우측에 있는 초록색 버튼을 누르면 나타난다





## 주의

나갈 때 `git push origin master` 했니?

올 때 `git pull origin master` 했니?