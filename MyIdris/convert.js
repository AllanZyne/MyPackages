const yaml = require('js-yaml');
const fs   = require('fs');
const util = require('util')



function handleCaptures(p) {
	let o = {};
	// console.log(p)
	for (let i = 0; i <= 100; ++i) {
		let pp = p[i];
		if (pp) {
			o[i] = pp.name;
		}
	}
	return o;
}

function handlePattern(p) {
	var oo = [];

	if (p.match) {
		var o = {};

		o.match = p.match;
		o.scope = p.name;

		oo.push(o);
	}

	if (p.begin) {
		var o = {};

		o.match = p.begin;
		if (p.beginCaptures) {
			o.captures = handleCaptures(p.beginCaptures);
		}

		var push = [];

		push.push({
			meta_scope: p.name
		});

		var end = {
			match: p.end,
			pop: true,
		};

		if (p.endCaptures) {
			end.captures = handleCaptures(p.endCaptures);
		}
		
		push.push(end);

		if (p.patterns) {
			for (let pp of p.patterns) {
				push = push.concat(handlePattern(pp));
			}
		}

		o.push = push;

		oo.push(o);
	}
	
	if (p.include) {
		var o = {};
		o.include = p.include.slice(1);
		oo.push(o);
	}

	if (!p.begin && p.patterns) {
		for (let pp of p.patterns) {
			oo = oo.concat(handlePattern(pp));
		}
	}

	return oo;
}


function convertSyntax(inputFile, outputFile) {
	let content = fs.readFileSync(inputFile, 'utf8');
	let data = JSON.parse(content);

	let sublime_syntax = {
		name: data.name,
		file_extensions: data.fileTypes,
		scope: data.scopeName,
		contexts: {
		}
	};

	let contexts = sublime_syntax.contexts;

	let main = [];

	for (let pp of data.patterns) {
		let r = handlePattern(pp);
		main = main.concat(r);
	}

	contexts.main = main;

	// console.log(util.inspect(main, false, null))

	for (let name in data.repository) {
		var pp = data.repository[name];
		let r = handlePattern(pp);
		contexts[name] = r;
	}

	// console.log(util.inspect(contexts, false, null))
	let dump = yaml.safeDump(sublime_syntax, {
		lineWidth: 100,
	});

	dump = dump.replace(/^(\s+)'(\d+)':/gm, '$1$2:');

	let dumpHead = '%YAML 1.2\n---\n# vscode-idris\n';

	fs.writeFileSync(outputFile, dumpHead + dump, 'utf8');
}

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

function handleSnippet(content) {
	let index = 1;
	let nameMap = {};

	// console.log();
	// console.log(content);
	// console.log('===========================')

	return content.replace(/\${([^}]*)}/g, function(full, match) {
		let seps = match.split(':');

		if (seps.length == 1) {
			let ii = nameMap[match];
			if (! ii) {
				ii = nameMap[match] = index++;
			}

			return '${' + ii + ':' + match + '}';
		}
		else if (seps.length == 2) {
			// console.log(parseInt(seps[0]) != NaN);
			if (! isNaN(parseInt(seps[0])))
				return;

			let ii = nameMap[seps[0]];
			if (! ii) {
				ii = nameMap[seps[0]] = index++;
			}
			return '${' + ii + ':' + seps[1] + '}';
		} else {
			console.error('!!!!!');
		}
	})
}

function convertSnippets(inputFile, outputFile) {
	let content = fs.readFileSync(inputFile, 'utf8');
	let data = JSON.parse(content);

	for (let desp in data) {
		let snip = data[desp];

		let sublime_snippet = `<snippet>
	<content><![CDATA[
${handleSnippet(snip.body.join('\n'))}
]]></content>
	<tabTrigger>${snip.prefix}</tabTrigger>
	<scope>source.idris</scope>
	<description>${desp}</description>
</snippet>
`;

		fs.writeFileSync(outputFile + toTitleCase(desp) + '.sublime-snippet', sublime_snippet, 'utf8');
	}
}

// convertSyntax('./idris.json', './idris.sublime-syntax');
// convertSyntax('./idris.literate.json', './idris.literate.sublime-syntax');
convertSnippets('./Snippets/idris.json', './Snippets/');
